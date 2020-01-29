FROM python:3.7.0
ENV PYTHONUNBUFFERED 1

RUN apt-get -y update && apt-get -y upgrade

RUN mkdir /app

WORKDIR /app
RUN pip install poetry
COPY ./.env.docker ./.env
COPY . /app/
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev
