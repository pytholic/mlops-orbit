"""Batch scoring script.

Created by @pytholic on 2024.03.10
"""

import os
import sys
import uuid

import mlflow
import pandas as pd
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GCS_ACCESS_TOKEN")


# Utility functions
def gen_uuids(n):
    ride_ids = []
    for i in range(n):
        ride_ids.append(str(uuid.uuid4()))
    return ride_ids


def read_dataframe(filename: str):
    df = pd.read_parquet(filename)

    df["duration"] = df.lpep_dropoff_datetime - df.lpep_pickup_datetime
    df.duration = df.duration.dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)]

    df["ride_id"] = gen_uuids(len(df))
    return df


def prepare_dictionaries(df: pd.DataFrame):
    categorical = ["PULocationID", "DOLocationID"]
    df[categorical] = df[categorical].astype(str)
    df["PU_DO"] = df["PULocationID"] + "_" + df["DOLocationID"]
    categorical = ["PU_DO"]
    numerical = ["trip_distance"]
    dicts = df[categorical + numerical].to_dict(orient="records")
    return dicts


def load_model(experiment_id, run_id):
    logged_model = (
        f"gs://pytholic-mlops-zoomcamp-artifacts/{experiment_id}/{run_id}/artifacts/model"
    )
    model = mlflow.pyfunc.load_model(logged_model)
    return model


def apply_model(input_file, experiment_id, run_id, output_file):

    print(f"Reading the data from {input_file}...")
    df = read_dataframe(input_file)
    dicts = prepare_dictionaries(df)

    print(f"Loading the model with RUN_ID={run_id}...")
    model = load_model(experiment_id, run_id)

    print("Applying the model...")
    y_pred = model.predict(dicts)

    print(f"Saving the result to {output_file}...")
    df_result = pd.DataFrame()
    df_result["ride_id"] = df["ride_id"]
    df_result["lpep_pickup_datetime"] = df["lpep_pickup_datetime"]
    df_result["PULocationID"] = df["PULocationID"]
    df_result["DOLocationID"] = df["DOLocationID"]
    df_result["actual_duration"] = df["duration"]
    df_result["predicted_duration"] = y_pred
    df_result["diff"] = df_result["actual_duration"] - df_result["predicted_duration"]
    df_result["model_version"] = run_id

    df_result.to_parquet(output_file, index=False)


def run():
    """Main function to load model/data and apply the model."""
    year = int(sys.argv[2])  # 2021
    month = int(sys.argv[3])  # 2
    taxi_type = sys.argv[1]  # "green"

    if not os.path.exists(f"output/{taxi_type}"):
        os.makedirs(f"output/{taxi_type}")

    input_file = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{taxi_type}_tripdata_{year:04d}-{month:02d}.parquet"  # download from link
    output_file = f"output/{taxi_type}/{year:04d}-{month:02d}.parquet"

    EXPERIMENT_ID = sys.argv[4]  # 1
    RUN_ID = sys.argv[5]  # "553def03f5224f649fe56bc1567daccc"

    apply_model(input_file, EXPERIMENT_ID, RUN_ID, output_file)


if __name__ == "__main__":
    run()
