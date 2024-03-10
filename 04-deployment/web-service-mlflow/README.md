# Web service deployment with model from model registry

## Setup

- Run an experiment with `RandomForestRegressor`
- Save `tracking data` in local storage
- Save `artifacts` in GCP Bucket
- Load the model from `model registry`
- Deploy the model as `web service`

## Create a GCP Bucket

Create a new Google Cloud Storage Bucket.

```
gcloud storage buckets create gs://BUCKET_NAME --project=PROJECT_ID --default-storage-class=STANDARD --location=BUCKET_LOCATION --uniform-bucket-level-access
```

```
gcloud storage buckets create gs://mlops-zoomcamp-artifacts --project=mlops-demo-408506 --default-storage-class=STANDARD --location=asia-northeast3 --uniform-bucket-level-access
```

## Start MLFlow server

```
mlflow server --host=0.0.0.0 \
--backend-store-uri=sqlite:///mfllow.db \
--default-artifact-root=gs://pytholic-mlops-zoomcamp-artifacts/
```

## Train the model and save in registry

Follow `04-deployment/web-service-model-registry/random-forest.ipynb`. We will make use of `sklearn pipeline`. Save the model in the registry bucket. We can also save the `dict_vectorizer.bin` and use it later for preprocessing, byt with `sklearn-pipeline` this process because embedded and cleaner for us. Tehrefore, we do not need to store it separately.

## Run Prediction

Make changes as shown in `04-deployment/web-service-mlflow/predict.py` to load model and dict vectorizer from mlflow server. I am loading model using the `RUN ID` but we can also use model `stage` for it.

We also need to install `mlflow` and `boto3` in our `deployment` environment.

```
pip install mlflow boto3 google-cloud-storage
```

Test.

```
python test.py


{'duration': 45.50965007660853, 'model_version': '553def03f5224f649fe56bc1567daccc'}
```

## Summarized steps

- Run the tracking server i.e. `mlflow server --host=0.0.0.0 --backend-store-uri=sqlite:///mfllow.db --default-artifact-root=gs://pytholic-mlops-zoomcamp-artifacts/`
- Run the prediction service i.e. `python predict.py`
- Send prediction request i.e. `python test.py`

## Removing dependence on the tracking server

What is the tracking serving is down? We cannot create a new instance of the `web-service` since we cannot connect to the tracking server. Consequently, we cannot send prediction requests to the service. So, we have become dependent on the tracking server, and this is a problem.

Instead of using `MLFLOW_TRACKIING_URI`, we can directly point it to load the model from `GCS bucket`.

```python
# MLFLOW_TRACKING_URI = "http://0.0.0.0:5000"
# mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# Load model
EXPERIMENT_ID = 1
RUN_ID = "553def03f5224f649fe56bc1567daccc"
logged_model = f"gs://pytholic-mlops-zoomcamp-artifacts/{EXPERIMENT_ID}/{RUN_ID}/artifacts/model"
# logged_model = f'runs:/{RUN_ID}/model'
model = mlflow.pyfunc.load_model(logged_model)
```
