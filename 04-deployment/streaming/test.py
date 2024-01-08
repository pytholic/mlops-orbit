import cloud_function

event = {
  "data": {
    "message": {
      "_comment": "data is base64 encoded string of 'Hello World'",
      "data": "ewogICAgInJpZGUiOiB7CiAgICAgICAgIlBVTG9jYXRpb25JRCI6IDEzMCwKICAgICAgICAiRE9Mb2NhdGlvbklEIjogMjA1LAogICAgICAgICJ0cmlwX2Rpc3RhbmNlIjogMy42NgogICAgfSwgCiAgICAicmlkZV9pZCI6IDEyMwp9"
    }
  },
  "type": "google.cloud.pubsub.topic.v1.messagePublished",
  "specversion": "1.0",
  "source": "//pubsub.googleapis.com/",
  "id": "1234567890"
}

res = cloud_function.predict_duration(event)
print(res)