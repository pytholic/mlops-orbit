# Overview
We can have failure points at different parts of our ML workflow, and things might break. It is important to deal with unexpected downtime and errors in an automatic fashion. 

# Prefect
**Prefect** orchestrates and observes out python workflows at scale. It consists of an `Orchestration API`, a `Database`, and a `UI`.
```
pip install -U prefect
```

## Terminology
**Task** - A discrete unit of work in a Prefect workflow<br>
**Flow** - Container for workflow logic<br>
**Subflow** - `Flow` called by another `flow`

## Steps

### Before Prefect
We will convert our notebook to python script which can be found in `03-workflow-orchestration/orchestrate_pre_prefect.py`. Run it and verify if mlflow and experiment are working.

```
python orchestrate_pre_prefect.py
```

In a separate terminal, run mlflow (make sure to forward the port in `~/.ssh/config`):
```
mlflow ui --backend-store-uri sqlite:///mlflow.db
```

## With Prefect
Convert normal functions to Prefect `task` and `flow` as in `03-workflow-orchestration/orchestrate.py`.