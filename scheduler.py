import time
import random
from datetime import datetime, timedelta
from db import Task, db
import schedule
import threading



def execute_task(task):
    task_id, task_name = task.id, task.name
    print(f"Executing Task {task_id}: {task_name}")

    with db.atomic():
        task = Task.get_by_id(task.id)  
        task.status = 'running'
        task.save()

    time.sleep(random.randint(1, 6))
    print(f"Task {task_id}: {task_name} completed")

    with db.atomic():
        task = Task.get_by_id(task.id)  
        task.status = 'completed'
        task.save()


def task_scheduler():
    while True:    
        current_time = datetime.now()
        tasks_to_execute = Task.select().where(Task.execution_time >= current_time)
        # print(f'Tasks to Execute: {[task.id for task in tasks_to_execute]}')

        threads = []

        for task in tasks_to_execute:
            time_until_execution = (task.execution_time - current_time).total_seconds()

            if time_until_execution > 0:
                print(f"Waiting for {time_until_execution} seconds until the next task execution.")
                time.sleep(time_until_execution)

            thread = threading.Thread(target=execute_task, args=(task,))
            thread.start()
            threads.append(thread)

    
        for thread in threads:
            thread.join()

        
        time.sleep(1)
