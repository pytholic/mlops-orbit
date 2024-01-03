import pickle
import mlflow
from flask import Flask, request, jsonify
from mlflow.tracking import MlflowClient


# MLFLOW_TRACKING_URI = "http://0.0.0.0:5000"
# mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# # Load dict vectorizer
# client = MlflowClient(MLFLOW_TRACKING_URI)
# path = client.download_artifacts(run_id=RUN_ID, path="dict_vectorizer.bin")
# print(F"Downloading the Dict Vectorizer to {path}..")

# with open(path, 'rb') as f_in:
#     dv = pickle.load(f_in)

# Load model
EXPERIMENT_ID = 1
RUN_ID = "553def03f5224f649fe56bc1567daccc"
logged_model = f"gs://pytholic-mlops-zoomcamp-artifacts/{EXPERIMENT_ID}/{RUN_ID}/artifacts/model"
# logged_model = f'runs:/{RUN_ID}/model'
model = mlflow.pyfunc.load_model(logged_model)

def prepare_features(ride):
    features = {}
    features["PU_DO"] = "%s_%s" % (ride["PULocationID"], ride["DOLocationID"])
    features["trip_distance"] = ride["trip_distance"]
    return features

def predict(features):
    # X = dv.transform(features) # use if not sklearn make_pipeline
    preds = model.predict(features)
    return float(preds[0]) # to avoid list


app = Flask("duration-prediction")

@app.route("/predict", methods=["POST"])
def predict_endpoint():
    ride = request.get_json()
    
    features = prepare_features(ride)
    pred = predict(ride)

    result = {
        "duration": pred,
        "model_version": RUN_ID
    }

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9696)