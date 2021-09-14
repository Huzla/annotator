FROM python:slim-buster

ENV FLASK_APP src
ENV STATIC_URL /static
ENV STATIC_PATH /var/www/app/static

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD flask run --host=0.0.0.0