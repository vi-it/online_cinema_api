FROM python:3.10

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install --upgrade pip && \
    pip3 install -r /app/requirements.txt --no-cache-dir

COPY . /app

CMD ["gunicorn", "main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]

