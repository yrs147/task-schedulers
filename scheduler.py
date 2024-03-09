import time
import random
from datetime import datetime
from db import Task, db
import threading
from tasks import calculate_next_execution_time


def execute_task(task):
    task_id, task_name = task.id, task.name
    print(f"Executing Task {task_id}: {task_name}")

    with db.atomic():
        task = Task.get_by_id(task.id)  
        task.status = 'running'
        task.save()

    time.sleep(random.randint(1, 6))
    print(f"Task {task_id}: {task_name} completed")

    if task.cron_schedule:

        task.execution_time = calculate_next_execution_time(task.cron_schedule)
        task.status = 'pending'
        with db.atomic():
            task.save()

        print(f"Next occurrence scheduled at {task.execution_time}")

    else:
        with db.atomic():
            task = Task.get_by_id(task.id)  
            task.status = 'completed'
            task.save()



def task_scheduler():
    while True:
        current_time = datetime.now()
        tasks_to_execute = Task.select().where(Task.execution_time <= current_time, Task.status == 'pending')

        threads = []

        for task in tasks_to_execute:
            thread = threading.Thread(target=execute_task, args=(task,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        time.sleep(1)

