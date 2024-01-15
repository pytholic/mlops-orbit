# Batch Deployment (Offline)
The ideal way of deployment for our app would be a `web-service`. However, here we can think of it in a way that we have an `actual` duration and a `predicted` duration, and we want to see how often they deviate from each other


1. Turn the notebook for training the model into a notebook for applying the model.
2. Convert notebook into a script
3. Clean and parametrize it

## Notebook conversion
Clean and remove extra stuff from the notebook. We will load the model and just apply it.

We will create a `result` dataframe.
- Includes `ride-id`. Since we don't have it in our original dataframe, we will add artificial ones. Normally, r`ride_ids` should already be there.