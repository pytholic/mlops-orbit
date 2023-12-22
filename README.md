# MLOps Pipeline
![Machine Learning Lifecycle](assets/mlops.png)

We will be training simple regression models on NYC taxi ride dataset and build MLOps pipeline including model training, hyperparameter optimization, experiment tracking, orchestrating, deployment, monitoring, etc. This repository is based on the MLOps course by DataTalks.Club.

# Notes
[Setting up a VM on GCP](notes/gcp_setup.md)<br>
[Dataset](notes/dataset.md)<br>
[MLFlow Experiment Tracking](notes/mlflow.md)<br>
[MLFlow Experiment Tracking on GCP](notes/mlflow_gcp.md)

# Setup

## Install requirements

Create environment

```
conda create -n exp-tracking python=3.9
```

Create `requirements.txt`

```
mlflow
jupyter
scikit-learn
pandas
seaborn
hyperopt
xgboost
```

Install requirements
```
pip install -r requirements.txt
```


## For remote VM
Forward MLflow port which is `5000`.
![mlflow port forwarding](assets/port2.png)

Also forward the port for `jupyter` if you are using it.
![jupyter port forwarding](assets/port1.png)