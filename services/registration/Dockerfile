FROM python:3.6.5-alpine3.7
RUN apk update
RUN apk add sudo gcc musl-dev --no-cache
COPY . /registration
RUN pip install --upgrade pip
RUN pip install -r /registration/requirements.txt
