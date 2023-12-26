# Overview
We can have failure points at different parts of our ML workflow, and things might break. It is important to deal with unexpected downtime and errors in an automatic fashion. 

# Simple orchestration
We will convert our notebook to python script which can be found in `03-workflow-orchestration/orchestrate_pre_prefect.py`. Run it and verify if mlflow and experiment are working.

```
python orchestrate_pre_prefect.py
```

In a separate terminal, run mlflow (make sure to forward the port in `~/.ssh/config`):
```
mlflow ui --backend-store-uri sqlite:///mlflow.db
```

# Prefect
**Prefect** orchestrates and observes out python workflows at scale. It consists of an `Orchestration API`, a `Database`, and a `UI`.
```
pip install -U prefect
```

## Terminology
**Task** - A discrete unit of work in a Prefect workflow<br>
**Flow** - Container for workflow logic<br>
**Subflow** - `Flow` called by another `flow`

## Orchestrating our workflow
Convert normal functions to Prefect `task` and `flow` as in `03-workflow-orchestration/orchestrate.py`.

Make sure to forward the prefect port (`127.0.0.1:4200`).
```
Host gcp-mlops-zoomcamp
    HostName xx.xx.xxx.xxx # VM Public IP
    User pytholic # VM user
    IdentityFile ~/.ssh/mlops-zoomcamp # Private SSH key file
    StrictHostKeyChecking no
    LocalForward 5000 0.0.0.0:5000
    LocalForward 4200 127.0.0.1:4200
```

Open prefect server in a new terminal.
```
prefect server start
```

Run the experiment.
```
python orchestrate.py
```

## Deploying workflow from local code

### Start prefect server
Open prefect server in a new terminal.
```
prefect server start
```

### 01-Initialize Prefect Project
Initialize prefect project (select `local` if prompted).
```
prefect init
```

### 02-Create a Work Pool
Create a `Work Pool` from the UI. Select `Local Subprocess` and give it a name. Click `Next` and hit `Create`.

### 03-Deploy your flow
```
prefect deploy myflow.py:main_flow -n <NAME> -p <WORK POOL NAME> 
```

### 04-Start the Work Pool
Run in a new terminal.
```
prefect worker start -p <WORK POOL NAME> -t process
```

### 05-Start a run of the deployment
Run in another terminal.
```
prefect deployment run 'main-flow/<deployment name>'
```
It will create a `flow run` for the deployment we created earlier. Our `Worker` will pick this up and execute our workflow. You can check this in the `Worker` terminal.

## Deploy from git

### Start prefect server
Open prefect server in a new terminal.
```
prefect server start
```

### 01-Clone the repo
Clone the repo with all the code.

### 02-Initialize Prefect Project
Initialize prefect project. This time select `git` instead of `local`.
```
prefect init
```

Next repeat the above steps. Make sure to push the `data` folder to git repo since prefect will clone it. We can see in the `Worker` terminal that it first clones the repo and then executes the workflow.