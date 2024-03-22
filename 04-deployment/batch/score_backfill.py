from datetime import date

from dateutil.relativedelta import relativedelta
from prefect import flow
from score_scheduled import ride_duration_prediction

# date(year=year, month=month, day=1)


@flow
def ride_duration_prediction_backfill():
    start_date = date(year=2021, month=3, day=1)
    end_date = date(year=2022, month=4, day=1)

    d = start_date
    while d <= end_date:
        ride_duration_prediction(
            taxi_type="green",
            run_id="553def03f5224f649fe56bc1567daccc",
            experiment_id="1",
            run_date=d,
        )

        d = d + relativedelta(months=1)


if __name__ == "__main__":
    ride_duration_prediction_backfill()
