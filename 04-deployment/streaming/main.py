import base64
import json

def prepare_features(ride):
    features = {}
    features["PU_DO"] = "%s_%s" % (ride["PULocationID"], ride["DOLocationID"])
    features["trip_distance"] = ride["trip_distance"]
    return features

def predict(features):
    preds = model.predict(features)
    return float(preds[0]) 

def predict_duration(event, context):
    data = base64.b64decode(event['data']).decode('utf-8')
    data = json.loads(data)
    ride = data["ride"]
    ride_id = data["ride_id"]
    features = prepare_features(ride)
    predicted_duration = round(predict(features))
    return_dict = {'ride_duration': predicted_duration,
                   "ride_id": ride_id}
    print(return_dict) #For Debugging