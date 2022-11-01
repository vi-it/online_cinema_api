FROM python:3.10

EXPOSE 8000

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install --upgrade pip && \
    pip3 install -r /app/requirements.txt --no-cache-dir

COPY . /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]