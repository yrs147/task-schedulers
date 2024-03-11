from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from tasks import create_task, read_all_tasks, update_task, delete_task, get_task_by_id

app = Flask(__name__)
api = Api(app)

class TaskResource(Resource):
    def get(self, task_id=None):
        if task_id is not None:
            task_data = get_task_by_id(task_id)
            if task_data:
                return jsonify(task_data)
            else:
                return jsonify({'message': f'Task with ID {task_id} not found'}), 404

        tasks = read_all_tasks()
        
        response_data = [
            {
                'id': task.id,
                'name': task.name,
                'status': task.status,
                'recurring': 'yes' if task.recurring else 'no',
                'cron_schedule': task.cron_schedule,
                'execution_time': task.execution_time.strftime('%Y-%m-%d %H:%M:%S')
            }
            for task in tasks
        ]

        return jsonify(response_data)
       
    def post(self):
        data = request.get_json()
        name = data.get('name')
        execution_time = data.get('execution_time')
        id = data.get('id')
        cron_schedule = data.get('cron_schedule')
        task = create_task(id, name, execution_time, cron_schedule)

        response_data = {
            'id': task.id,
            'name': task.name,
            'status': task.status,
            'recurring': task.recurring
        }

        if task.recurring:
            response_data['cron_schedule'] = task.cron_schedule
        else:
            response_data['execution_time'] = task.execution_time.strftime('%Y-%m-%d %H:%M:%S')

        return response_data, 201

    
    def put(self, task_id):
        data = request.get_json()
        name = data.get('name')
        execution_time = data.get('execution_time')
        cron_schedule= data.get('cron_schedule')
        
        update_task(task_id, name, execution_time,cron_schedule)
        return {'message': f'Task {task_id} updated successfully'}

    def delete(self, task_id):
        delete_task(task_id)
        return {'message': f'Task {task_id} deleted successfully'}
    

api.add_resource(TaskResource, '/tasks', '/tasks/<int:task_id>')


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
