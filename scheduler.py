import time
import random
from datetime import datetime, timedelta
from db import Task
import schedule

def execute_task(task_id,task_name):
    print(f"Executing Task {task_id}: {task_name}")
    time.sleep(random.randint(1,6))
    print(f"Task {task_id}: {task_name} completed")

def task_scheduler():
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')    
    tasks_to_execute = Task.select().where(Task.execution_time <=current_time)

    for task in tasks_to_execute:
        task_id,task_name = task.id, task.name
 

def schedule_tasks():
    schedule.every(1).seconds.do(task_scheduler)
    while True:
        schedule.run_pending()  
        time.sleep(1)     