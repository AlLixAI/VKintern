FROM python:3.8

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt --verbose

COPY . .

# CMD ["sh", "/app.sh"]

CMD gunicorn rest.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000