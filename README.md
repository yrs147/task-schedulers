# Task Scheduler Project

  
## Overview


The Task Scheduler Project is a powerful task scheduling system designed to perform tasks at specific timestamps or recurring intervals. It provides a flexible and user-friendly interface for scheduling and managing tasks, with support for various deployment options.

  

## Features

  
- **Flask API for CRUD Operations:** Manage tasks through a RESTful API, allowing Create, Read, Update, and Delete (CRUD) operations on the task database.

- **Command Line Interface (CLI):** Interact with the scheduler through a command-line interface, enabling users to create, update, read, and delete tasks.

- **Parallel Task Execution:** Supports parallel execution of tasks, allowing for efficient and concurrent processing.

- **Recurring Task Support:** - Users can schedule recurring tasks using cron format via the API, CLI, or Kubernetes Jobs.

- **Kubernetes Deployment:** - Easily deploy the scheduler and MySQL database using Helm Charts, simplifying the deployment process.

  

## Installation

### Deploying with Helm Chart


1. Clone the repository:

```bash

git clone https://github.com/yrs147/task-schedulers.git

cd repository

```

  

2. Deploy the scheduler and MySQL with Helm:

```bash

helm install myrelease ./project-setup-chart

```
# Database Schema


| Field           | Type       | Constraints      |
|-----------------|------------|------------------|
| id              | integer    | primary key      |
| name            | varchar    |                  |
| execution_time  | datetime   |                  |
| status          | varchar    |                  |
| recurring       | varchar    |                  |
| cron_schedule   | varchar    |                  |
  

# Usage

## API

  
| Method | Route               | Description                      |
|--------|---------------------|----------------------------------|
| GET    | /api/tasks          | Get a list of tasks               |
| GET    | /api/tasks/{taskId} | Get details of a specific task    |
| POST   | /api/tasks          | Create a new task                 |
| PUT    | /api/tasks/{taskId} | Update details of a specific task |
| DELETE | /api/tasks/{taskId} | Delete a specific task            |


  

1. Port forward the pod to make the api acessible on `localhost:5000`

```bash
kubectl port-forward myrelease-taskchart-scheduler 5000:5000
```

2. Now from another terminal window make a request on the respective path


### Create a new task (`POST /api/tasks`)

**Path** - `http://localhost:5000/tasks`

**Request Body(For Recurring Tasks):**

```
{   
    "id": "1001"
    "name": "Task 1001",   
    "cron_schedule": "*/2 * * * *",   
}
```

- `id` (integer): The id of the task.
- `name` (string): The name of the task.
- `cron_schedule` (string): The cron schedule for task execution.


**Request Body(For Non-Recurring Tasks):**

```
{   
    "id": "1001"
    "name": "Task 1001",   
    "execution_time": "2024-03-11 00:06:00",   
}
```

- `id` (integer): The id of the task.
- `name` (string): The name of the task.
- `execution_time` (string): The execution time for non-recurring tasks.


### Update details of a  task (`PUT /api/tasks/{taskId}`)

**Path** - `http://localhost:5000/tasks/{task_id}`

**Request Body(Recurring Tasks):**

Can update both or either one

```
{   
    "name": "Task 1001",   
    "execution_time": "2024-03-11 00:06:00",   
}
```

**Request Body(Non Recurring Tasks):**

Can update both or either one

```
{   
    "name": "Task 1001",   
    "cron_schedule": "* * * * *",   
}
```

### GetById and Delete Does not require a request body , just append the task_id at the end of their respective path
**Path** - `http://localhost:5000/tasks/{task_id}`


## CLI

### - Create a new task(Recurring):

```
kubectl exec myrelease-taskchart-scheduler -- python ./main.py create --name TaskName --cron_schedule '*/2 * * * *'  
```

### - Create a new task(Non Recurring):

```
kubectl exec myrelease-taskchart-scheduler -- python ./main.py create --name TaskName  --execution_time '2024-03-11 00:06:00' 
```


### - Get Tasks:

```
kubectl exec myrelease-taskchart-scheduler -- python ./main.py view
```

### - Get a Specific Tasks by Id:

```
kubectl exec myrelease-taskchart-scheduler -- python ./main.py get --id="ID"
```


### - Update a  task(Recurring):

`id` is req to get the task and then you can update either of `name` or `cron_schedule`

```
kubectl exec myrelease-taskchart-scheduler -- python ./main.py update  --id=1087 --cron_schedule '*/2 * * * *'  
```

### - Update a  task(Non Recurring):

`id` is req to get the task and then you can update either of `name` or `execution_time`


```
kubectl exec myrelease-taskchart-scheduler -- python ./main.py update --id=8765 --name TaskName  --execution_time '2024-03-11 00:06:00' 
```

### - Delete a Task:

```
kubectl exec myrelease-taskchart-scheduler -- python ./main.py delete --id=5423
```

## Kubernetes Jobs

**You can also use Kubernetes jobs to create tasks using Kubernetes job helm charts***


### - Create Non Recurring Task:

```
helm install create-non-recurring-task-release ./create-non-recurring  --set nonRecurringTaskJob.id="ID" --set nonRecurringTaskJob.name="TASK_NAME" --set nonRecurringTaskJob.executionTime="YYYY-MM-DD HH:MM:SS"
```

### - Create Non Recurring Task:

```
helm install create-recurring-task-release ./create-recurring/ --set createTaskJob.id="ID" --set createTaskJob.name="TASK_NAME" --set createTaskJob.cronSchedule="* * * * *"
```
## Cron Schedule Examples

- Daily: `0 0 * * *`
- Weekly: `0 0 * * 0`
- Monthly: `0 0 1 * *`
- Yearly: `0 0 1 1 *`
