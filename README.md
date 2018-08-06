# CruzHacks 2019 Backend Services

## Summary

This repo defines backend services for use within Docker.  Docker abstracts away your environment specific settings so that your code runs the same everywhere.  Each service's build environment is defined in a `Dockerfile`.  We bring up all of the services with `docker-compose.yml`.

NGINX is used as a reverse proxy into each service's web server.  For registration, the Flask app is served with gunicorn to be production-ready and separate from all other services.

## Getting Started

Build containers for each service and run them:

```bash
docker-compose up --build
```

Then hit your endpoints with the service name prefixing each route:

```bash
curl -X GET localhost/registration
```

Note that the default port is set to 80 (the same as HTTP) for production.  Any requests to localhost on port 80 will go to these backend services.  If this is a problem for you locally, change the NGINX host port (format is `HOST:CONTAINER`) in docker-compose.yml (for development only).

Replace GET with whatever HTTP verb you want to hit the endpoint with.  You may need the `--data` argument (for POSTs usually), check `man curl` for more details.

The port number varies depending on the service.  Verify that you're hitting the right port by checking for the service's container in `docker ps`. 

### Prerequisities

- [Docker](https://docs.docker.com/install/#supported-platforms)

### Installing

A step by step series of examples that tell you have to get a development env running

Stay what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

```bash
pytest
```

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment


