FROM python:3.7-slim
ENV PYTHONUNBUFFERED=1
ARG PIPENV_ARGS=""

ARG CONFIG=production
ENV GUNICORN_CONFIG=${CONFIG}

ADD requirements.txt /requirements.txt
RUN pip install -r requirements.txt

WORKDIR /app
ADD . /app

RUN adduser --disabled-login --system --gecos 'App User' app
USER app

CMD gunicorn src:application --config src/config/gunicorn/$GUNICORN_CONFIG.py --log-file=-
