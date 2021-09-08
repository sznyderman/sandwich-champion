FROM python:3.9-slim-buster

COPY requirements-app.txt /tmp/
COPY requirements-dev.txt /tmp/
RUN pip install -r /tmp/requirements-app.txt -r /tmp/requirements-dev.txt

RUN mkdir -p /src
COPY src/ /src/
RUN pip install -e /src
COPY tests/ /tests/

WORKDIR /src
