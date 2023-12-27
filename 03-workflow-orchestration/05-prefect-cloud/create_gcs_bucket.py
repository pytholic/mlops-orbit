import json
import os
from time import sleep
from prefect_gcp import GcpCredentials, GcsBucket
from google.cloud import storage
from google.cloud.storage.constants import PUBLIC_ACCESS_PREVENTION_ENFORCED

KEY_PATH = "/home/pytholic/service_account_key.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/pytholic/service_account_key.json"


def create_gcp_creds_block():
    json_file_path = KEY_PATH
    with open(json_file_path) as f:
        service_account_info = json.load(f)

    my_gcp_creds_obj = GcpCredentials(service_account_info=service_account_info)
    my_gcp_creds_obj.save(name="my-gcp-creds", overwrite=True)


def create_gcs_bucket_block(bucket_name="orchestration-bucket-2"):
    gcp_creds = GcpCredentials.load("my-gcp-creds")

    # The following line creates a bucket in Google Cloud Storage. You might want to replace this with the
    # appropriate code if the bucket already exists.
    cloud_storage_client = gcp_creds.get_cloud_storage_client()
    cloud_storage_client.create_bucket(bucket_name, location="ASIA-NORTHEAST3")

    my_gcs_bucket_obj = GcsBucket(
        bucket=bucket_name, gcp_credentials=gcp_creds
    )
    
    my_gcs_bucket_obj.save(name=bucket_name, overwrite=True)

    # Change attributes
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    bucket.iam_configuration.public_access_prevention = (
        PUBLIC_ACCESS_PREVENTION_ENFORCED
    )
    bucket.iam_configuration.uniform_bucket_level_access_enabled = True
    bucket.patch()


if __name__ == "__main__":
    create_gcp_creds_block()
    sleep(5)
    create_gcs_bucket_block()