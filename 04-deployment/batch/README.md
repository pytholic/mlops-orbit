# Batch Deployment (Offline)
The ideal way of deployment for our app would be a `web-service`. However, here we can think of it in a way that we have an `actual` duration and a `predicted` duration, and we want to see how often they deviate from each other


1. Turn the notebook for training the model into a notebook for applying the model.
2. Convert notebook into a script
3. Clean and parametrize it

## Notebook conversion
Clean and remove extra stuff from the notebook. We will load the model and just apply it. Check `score.ipynb`.

1. We will create a `result` dataframe and save it.
   - We will include a `ride-id` so that we can relate the predictions with the correct ride. Since we don't have it in our original dataframe, we will add artificial ones. Normally, `ride_ids` should already be there.
   - We will also include some other information like pickup and drop-off location, actual dutation, predicted duration, and the difference between the two durations.

2. Convert everything to functions.

## Convert the notebook into a script.
```
jupyter nbconvert --to script score.ipynb
```

## Clean and parameterize
Clean and parameterize the script like `score.py`.

Run it.
```
python score.py green <YEAR> <MONTH> <EXPERIMENT ID> <RUN ID>
python score.py green 2021 2 1 553def03f5224f649fe56bc1567daccc
```

Output logs.
```
Reading the data from https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2021-01.parquet...
Loading the model with RUN_ID=553def03f5224f649fe56bc1567daccc...
Applying the model...
Saving the result to output/green/2021-01.parquet...
```

## Further Steps
We can package our dependencies, create a docker container, and schedule it as kubernetes job or AWS batch etc.

