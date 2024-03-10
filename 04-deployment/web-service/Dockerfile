FROM python:3.9.18-slim

RUN pip install -U pip

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY [ "predict.py", "lin_reg.bin", "./" ]

EXPOSE 9696

ENTRYPOINT [ "gunicorn", "--bind=0.0.0.0:9696", "predict:app" ]
