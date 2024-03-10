import requests

ride = {"PULocationID": 10, "DOLocationID": 50, "trip_distance": 40}

# url = "http://127.0.0.1:9696/predict"
# url = "http://172.18.0.2:30001/predict" # Kind Kubernetes
url = "http://34.64.41.41/predict"  # GKE
response = requests.post(url, json=ride)
print(response.json())

# features = predict.prepare_features(ride)
# pred = predict.predict(ride)
# print(pred)
