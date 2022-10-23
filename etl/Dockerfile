FROM python:3.10

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements requirements
COPY .env .env
COPY .env.example .env.example

RUN  pip install --upgrade pip \
     && pip install -r requirements

COPY . .

#ENTRYPOINT ["python", "main.py"]
