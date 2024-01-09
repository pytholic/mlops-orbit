FROM python:3.9-slim

RUN pip install -U pip

WORKDIR /app

COPY ["cloud_function.py", "service_account_key.json", "requirements.txt", "./"]

RUN pip install -r requirements.txt

ENV GOOGLE_APPLICATION_CREDENTIALS="./service_account_key.json"

CMD [ "python", "cloud_function.py" ] 