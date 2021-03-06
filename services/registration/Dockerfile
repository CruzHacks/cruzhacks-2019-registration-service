# Build environment initialization.
FROM python:3.6.5-alpine3.7
RUN apk update
RUN apk add bash sudo gcc musl-dev postgresql postgresql-dev libffi-dev --no-cache

RUN mkdir -p /usr/src/app/registration
COPY ./ /usr/src/app/registration

# Define the app as a Python package.
RUN ["/bin/bash", "-c", "touch usr/src/app/__init__.py"]

# Install Python dependencies.
COPY ./requirements.txt /usr/src/app/registration/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /usr/src/app/registration/requirements.txt

# Config settings to load BEFORE the entry point of the container.
ENV GUNICORN_AUTO_RELOAD="OFF"
ENV PYTHONPATH="$PYTHONPATH:/usr/src/app:/usr/local/lib:/usr/local/bin"

CMD /usr/src/app/registration/wait-for-postgres.sh gunicorn registration.wsgi --config=/usr/src/app/registration/gunicorn.py
