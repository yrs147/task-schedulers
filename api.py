from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from tasks import create_task, read_all_tasks, update_task, delete_task
from prettytable import PrettyTable

app = Flask(__name__)
api = Api(app)

class TaskResource(Resource):
    def get(self,task_id=None):
        tasks = read_all_tasks()
        return jsonify([{'id': task.id, 'name': task.name, 'execution_time': task.execution_time.strftime('%Y-%m-%d %H:%M:%S')} for task in tasks])
       


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
        execution_time = data.get('execution_time')
        
        update_task(task_id, name, execution_time)
        return {'message': f'Task {task_id} updated successfully'}

    def delete(self, task_id):
        delete_task(task_id)
        return {'message': f'Task {task_id} deleted successfully'}
    

api.add_resource(TaskResource, '/tasks', '/tasks/<int:task_id>')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=False)
