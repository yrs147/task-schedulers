from db import Task, db
from datetime import datetime, timedelta
from crontab import CronTab

def create_task(id, name, execution_time, cron_schedule):
    with db.atomic():
        recurring = 'yes' if cron_schedule else 'no'

        if cron_schedule:
            execution_time = calculate_next_execution_time(cron_schedule)

        return Task.create(id=id, name=name, execution_time=execution_time, cron_schedule=cron_schedule, recurring=recurring)

def read_all_tasks():
    with db.atomic():
        return Task.select()

def get_task_by_id(task_id):
    with db.atomic():
        task = Task.get_by_id(task_id)
        return {
            'id': task.id,
            'name': task.name,
            'status': task.status,
            'recurring': 'yes' if task.recurring else 'no',
            'cron_schedule': task.cron_schedule,
            'execution_time': task.execution_time.strftime('%Y-%m-%d %H:%M:%S')
        }

def update_task(task_id, name, execution_time, cron_schedule):
    with db.atomic():
        task = Task.get_by_id(task_id)

        if task.recurring == 'yes' and execution_time is not None:
            raise ValueError("Cannot change a recurring task to non-recurring")
        
        if task.recurring == 'no' and cron_schedule is not None:
            raise ValueError("Cannot change a non-recurring task to recurring or vice versa.")

        if cron_schedule is not None:
            task.cron_schedule = cron_schedule
            task.execution_time = calculate_next_execution_time(cron_schedule)
            task.recurring = 'yes'

        if name is not None:
            task.name = name

        if execution_time is not None:
            task.execution_time = datetime.strptime(execution_time, '%Y-%m-%d %H:%M:%S')
            task.cron_schedule = None  
            task.recurring = 'no'

        task.save()

def delete_task(task_id):
    with db.atomic():
        Task.get_by_id(task_id).delete_instance()

def calculate_next_execution_time(cron_schedule):
    now = datetime.now()
    cron = CronTab(cron_schedule)
    next_execution = cron.next(default_utc=False)
    return now + timedelta(seconds=next_execution)
