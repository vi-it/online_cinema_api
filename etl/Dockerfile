FROM python:3.10

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt
COPY .env .env

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt

COPY . .

# prevent the container from exiting:
CMD ["tail", "-F", "anything"]
# run the script:
CMD ["python", "main.py"]
