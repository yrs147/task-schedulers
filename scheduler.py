import time
import random
from datetime import datetime, timedelta
from db import Task
import schedule
import threading

def execute_task(task):
    task_id, task_name = task.id, task.name
    print(f"Executing Task {task_id}: {task_name}")
    
    task.status = 'running'
    task.save()

    time.sleep(random.randint(1, 6))
    print(f"Task {task_id}: {task_name} completed")

    # Update task status to 'completed'
    task.status = 'completed'
    task.save()

def task_scheduler():
    while True:    
        current_time = datetime.now()
        tasks_to_execute = Task.select().where(Task.execution_time >= current_time)
        print(f'Tasks to Execute: {[task.id for task in tasks_to_execute]}')

        for task in tasks_to_execute:
            time_until_execution = (task.execution_time - current_time).total_seconds()

            if time_until_execution > 0:
                print(f"Waiting for {time_until_execution} seconds until the next task execution.")
                time.sleep(time_until_execution)

            execute_task(task)

def schedule_tasks():
    # while True:
    #     # Check for new tasks in each iteration
    task_scheduler()
    time.sleep(1)     

if __name__ == '__main__':
    # Schedule the task_scheduler function to run every second
    schedule.every(1).seconds.do(schedule_tasks)

    # # Run the schedule_tasks function in a separate thread
    # threading.Thread(target=schedule_tasks).start()

    while True:
        # Run pending scheduled tasks
        schedule.run_pending()
        time.sleep(1)
