
FROM ubuntu:19.04
FROM python:3.7-alpine
WORKDIR /appsec4
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_RUN_PORT=8080
RUN apk --update add python py-pip openssl ca-certificates py-openssl wget
RUN mkdir /app
ADD requirements.txt /app/requirements.txt
WORKDIR /app
RUN apk --update add python py-pip openssl ca-certificates py-openssl wget
RUN apk --update add --virtual build-dependencies libffi-dev openssl-dev python-dev py-pip build-base \
  && pip install --upgrade pip \
  && pip install -r requirements.txt \
  && apk del build-dependencies
COPY requirements.txt /tmp
WORKDIR /tmp
RUN pip3 install -r requirements.txt
COPY . .
CMD ["flask", "run"]
