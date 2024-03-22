#!/usr/bin/env python

import os
import sys
import uuid
from datetime import date
from typing import Union

import mlflow
import pandas as pd
from dateutil.relativedelta import relativedelta
from dotenv import find_dotenv, load_dotenv
from prefect import (
    flow,
    get_run_logger,
    task,
)
from prefect.context import get_run_context

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


@task
def apply_model(input_file, experiment_id, run_id, output_file):
    logger = get_run_logger()

    logger.info(f"Reading the data from {input_file}...")
    df = read_dataframe(input_file)
    dicts = prepare_dictionaries(df)

    logger.info(f"Loading the model with RUN_ID={run_id}...")
    model = load_model(experiment_id, run_id)

    logger.info("Applying the model...")
    y_pred = model.predict(dicts)

    logger.info(f"Saving the result to {output_file}...")
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


def get_paths(run_date, taxi_type, run_id):
    prev_month = run_date - relativedelta(months=1)
    year = prev_month.year
    month = prev_month.month

    input_file = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{taxi_type}_tripdata_{year:04d}-{month:02d}.parquet"

    # input_file = (
    #     f"gs://taxi-ride-prediction/data/{taxi_type}_tripdata_{year:04d}-{month:02d}.parquet"
    # )
    output_file = f"gs://taxi-ride-prediction/output/taxi_type={taxi_type}/year={year:04d}/month={month:02d}/{run_id}.parquet"

    return input_file, output_file


@flow
def ride_duration_prediction(
    taxi_type: str, run_id: str, experiment_id: Union[str, int], run_date: date = None
):
    if run_date is None:
        ctx = get_run_context()
        run_date = ctx.flow_run.expected_start_time

    input_file, output_file = get_paths(run_date, taxi_type, run_id)

    apply_model(
        input_file=input_file, experiment_id=experiment_id, run_id=run_id, output_file=output_file
    )


def run():
    """Main function to load model/data and apply the model."""
    year = int(sys.argv[2])  # 2021
    month = int(sys.argv[3])  # 2
    taxi_type = sys.argv[1]  # "green"
    EXPERIMENT_ID = sys.argv[4]  # 1
    RUN_ID = sys.argv[5]  # "553def03f5224f649fe56bc1567daccc"

    ride_duration_prediction(
        taxi_type=taxi_type,
        run_id=RUN_ID,
        experiment_id=EXPERIMENT_ID,
        run_date=date(year=year, month=month, day=1),
    )


if __name__ == "__main__":
    run()
