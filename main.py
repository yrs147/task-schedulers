from db import db, Task
from tasks import create_task, read_all_tasks, update_task, delete_task
from scheduler import task_scheduler
from api import app
from prettytable import PrettyTable

import threading
import argparse

def tabulate_tasks(tasks):
    table = PrettyTable()
    table.field_names = ["Sno", "ID", "Name", "Execution Time", "Status"]

    for sno, task in enumerate(tasks, start=1):
        table.add_row([sno, task.id, task.name, task.execution_time.strftime('%Y-%m-%d %H:%M:%S'), task.status])

    return table.get_string()

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
        print(tabulate_tasks(tasks))
    elif args.command == 'create':
        create_task(args.id, args.name, args.execution_time)
        print('Task created successfully.')
    elif args.command == 'update':
        update_task(args.id, args.name, args.execution_time)
        print(f'Task {args.id} updated successfully.')
    elif args.command == 'delete':
        delete_task(args.id)
        print(f'Task {args.id} deleted successfully.')

if __name__ == '__main__':
    main()
