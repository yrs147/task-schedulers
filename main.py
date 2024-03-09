# main.py
from db import db, Task
from tasks import create_task, read_all_tasks, update_task, delete_task
from scheduler import task_scheduler
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from prettytable import PrettyTable

import threading
import argparse

app = Flask(__name__)
api = Api(app)

class TaskResource(Resource):
    def get(self):
        tasks = read_all_tasks()
        return self.tabulate_tasks(tasks)

    def post(self):
        data = request.get_json()
        name = data.get('name')
        execution_time = data.get('execution_time')
        id = data.get('id')
        task = create_task(id, name, execution_time)
        return {'id': task.id, 'name': task.name, 'execution_time': task.execution_time.strftime('%Y-%m-%d %H:%M:%S'), 'status': task.status}, 201

    def put(self, task_id):
        data = request.get_json()
        name = data.get('name')
        update_task(task_id, name)
        return {'message': f'Task {task_id} updated successfully'}

    def delete(self, task_id):
        delete_task(task_id)
        return {'message': f'Task {task_id} deleted successfully'}
    
    def tabulate_tasks(self, tasks):
        table = PrettyTable()
        table.field_names = ["Sno", "ID", "Name", "Execution Time", "Status"]

        for sno, task in enumerate(tasks, start=1):
            table.add_row([sno, task.id, task.name, task.execution_time.strftime('%Y-%m-%d %H:%M:%S'), task.status])

        return table.get_string()


api.add_resource(TaskResource, '/tasks', '/tasks/<int:task_id>')

def main():
    parser = argparse.ArgumentParser(description='Task Management Application')
    parser.add_argument('command', choices=['run', 'view', 'create', 'update', 'delete'], help='Command to execute')

    # Task-related arguments
    parser.add_argument('--id', type=int, help='Task ID')
    parser.add_argument('--name', type=str, help='Task Name')
    parser.add_argument('--execution_time', type=str, help='Task Execution Time (YYYY-MM-DD HH:MM:SS)')

    args = parser.parse_args()

    if args.command == 'run':
        if not db.is_closed():
            # If the database is already connected, close the existing connection
            db.close()

        db.connect()
        db.create_tables([Task], safe=True)
        threading.Thread(target=task_scheduler).start()

        app.run(debug=False)
    elif args.command == 'view':
        tasks = read_all_tasks()
        print(TaskResource().tabulate_tasks(tasks))
    elif args.command == 'create':
        create_task(args.id, args.name, args.execution_time)
        print('Task created successfully.')
    elif args.command == 'update':
        update_task(args.id, args.name)
        print(f'Task {args.id} updated successfully.')
    elif args.command == 'delete':
        delete_task(args.id)
        print(f'Task {args.id} deleted successfully.')

if __name__ == '__main__':
    main()
