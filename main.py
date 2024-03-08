from db import db , Task
from tasks import create_task, read_all_tasks, update_task, delete_task
from scheduler import task_scheduler
from flask import Flask, request, jsonify
from flask_restful import Api, Resource

import threading

app = Flask(__name__)
api = Api(app)

class TaskResource(Resource):
    def get(self):
        tasks = read_all_tasks()
        return jsonify([{'id': task.id, 'name': task.name, 'execution_time': task.execution_time.strftime('%Y-%m-%d %H:%M:%S'), 'status': task.status} for task in tasks])

    def post(self):
        data = request.get_json()
        name = data.get('name')
        execution_time = data.get('execution_time')
        id = data.get('id')
        task = create_task(id,name,execution_time)
        return {'id': task.id, 'name': task.name, 'execution_time': task.execution_time.strftime('%Y-%m-%d %H:%M:%S'), 'status': task.status}, 201

    def put(self,task_id):
        data = request.get_json()    
        name = data.get('name')
        update_task(task_id,name)
        return {'message':f'Task {task_id} updated successfully'}

    def delete(self,task_id):
        delete_task(task_id)
        return{'message':f'Task {task_id} deleted successfully'}

api.add_resource(TaskResource, '/tasks', '/tasks/<int:task_id>')

if __name__ == '__main__':

    if not db.is_closed():
        # If the database is already connected, close the existing connection
        db.close()

    db.connect()
    db.create_tables([Task], safe=True)
    threading.Thread(target=task_scheduler).start()

    app.run(debug=False)

