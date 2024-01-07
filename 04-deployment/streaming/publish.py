import os
import json
import base64

from google.cloud import pubsub_v1

#1. Initialize Client
publisher = pubsub_v1.PublisherClient()
PROJECT_ID = os.getenv("PROJECT_ID")
TOPIC_NAME = os.getenv("BACKEND_PUSH_STREAM")

topic_path = publisher.topic_path(PROJECT_ID, TOPIC_NAME)

def send(message_json):
        #2. Encode the message json
        message_bytes = message_json.encode('utf-8')
        
        try:
            #3. Publish the message to the topic
            publish_future = publisher.publish(topic_path, data=message_bytes)
            #4. Verify that the message has arrived
            publish_future.result()  # Verify the publish succeeded

            return 'Message published.'
        except Exception as e:
            print(e)
            return (e,500)

data = {
    "ride": {
        "PULocationID": 130,
        "DOLocationID": 205,
        "trip_distance": 3.66
    }, 
    "ride_id": 123
}

ride = json.dumps(ride)
send(ride)