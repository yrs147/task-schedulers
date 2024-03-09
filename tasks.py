# task.py
from db import Task, db
from datetime import datetime

def create_task(id, name, execution_time):
    execution_time = datetime.strptime(execution_time, '%Y-%m-%d %H:%M:%S')
    
    with db.atomic():
        return Task.create(id=id, name=name, execution_time=execution_time)

def read_all_tasks():
    with db.atomic():
        return Task.select()

def update_task(task_id, name):
    with db.atomic():
        task = Task.get_by_id(task_id)
        task.name = name
        task.save()

def delete_task(task_id):
    with db.atomic():
        Task.get_by_id(task_id).delete_instance()
