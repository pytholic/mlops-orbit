# Dataset

Website

https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

<br>
Download 2021 data for the Green Taxi (January and February)

```
mkdir data
wget https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2021-01.parquet
wget https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2021-02.parquet
```

<br>
Reference

https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_green.pdf

<br>
Reading parquet data

```
pip install pyarrow
```

```
import pandas as pd
df = pd.read_parquet("./data/green_tripdata_2022-01.parquet")
```