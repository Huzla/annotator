FROM python:slim-buster

RUN pip install flask

ENV FLASK_APP src
ENV STATIC_URL /static
ENV STATIC_PATH /var/www/app/static

COPY . /app
WORKDIR /app

ENTRYPOINT flask run --host=0.0.0.0