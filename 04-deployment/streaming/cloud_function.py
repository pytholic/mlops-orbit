import base64
import json
import os

import functions_framework
import mlflow
from google.cloud import pubsub_v1

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/pytholic/service_account_key.json"

publisher = pubsub_v1.PublisherClient()
PROJECT_ID = os.getenv("PROJECT_ID", "mlops-demo-408506")
TOPIC_NAME = os.getenv("PUBLISH_STREAM", "ride-predictions")
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_NAME)

# Load model
EXPERIMENT_ID = 1
RUN_ID = "553def03f5224f649fe56bc1567daccc"
logged_model = f"gs://pytholic-mlops-zoomcamp-artifacts/{EXPERIMENT_ID}/{RUN_ID}/artifacts/model"
model = mlflow.pyfunc.load_model(logged_model)


def prepare_features(ride):
    features = {}
    features["PU_DO"] = "{}_{}".format(ride["PULocationID"], ride["DOLocationID"])
    features["trip_distance"] = ride["trip_distance"]
    return features


def predict(features):
    pred = model.predict(features)
    return pred[0]


def publish_to_topic(project_id, topic_name, message_json):
    # Encode the message json
    message_encoded = json.dumps(message_json).encode("utf-8")
    # Publish the message to the topic
    future = publisher.publish(topic_path, data=message_encoded)
    # Verify that the message has arrived
    print(future.result())


@functions_framework.cloud_event
def predict_duration(cloud_event):
    decoded = base64.b64decode(cloud_event.data["message"]["data"])
    data = json.loads(decoded)
    ride = data["ride"]
    ride_id = data["ride_id"]
    features = prepare_features(ride)
    predicted_duration = round(predict(features))
    prediction = {
        "model": "ride_duration_prediction_model",
        "version": 123,
        "prediction": {"ride_duration": predicted_duration, "ride_id": ride_id},
    }

    # Publish the result to another Pub/Sub topic
    publish_to_topic(PROJECT_ID, TOPIC_NAME, prediction)

    return prediction
