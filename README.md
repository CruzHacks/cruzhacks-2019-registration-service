# CruzHacks 2019 Backend Services

## Summary

This repo defines backend services for use within Docker.  Docker abstracts away your environment specific settings so that your code runs the same everywhere.  Each service's build environment is defined in a `Dockerfile`.  We bring up all of the services with `docker-compose.yaml`.

NGINX is used as a reverse proxy into each service's web server.  For registration, the Flask app is served with gunicorn to be production-ready and separate from all other services.  Postgres is configured to be persistent, so killing your Postgres container and restarting it will preserve the data.

## Getting Started

Build containers for each service and run them:

```bash
docker-compose up --build
```

Then hit your endpoints with the service name prefixing each route:

```bash
curl localhost/registration
curl -X POST localhost/registration
curl -X GET localhost/registration
```

Note that the default port is set to 80 (the same as HTTP) for production.  Any requests to localhost on port 80 will go to these backend services.  If this is a problem for you locally, change the NGINX host port (format is `HOST:CONTAINER`) in docker-compose.yml (for development only).

Replace GET with whatever HTTP verb you want to hit the endpoint with.  You may need the `--data` argument (for POSTs usually), check `man curl` for more details.

The port number varies depending on the service.  Verify that you're hitting the right port by checking for the service's container in `docker ps`. 

To ease development, set `ENV GUNICORN_AUTO_RELOAD="on"` at the bottom of `./services/registration/Dockerfile`.  This will allow you to make changes in source code that is reflected on your running Docker container.  Please toggle this to `ENV GUNICORN_AUTO_RELOAD="off"` when you are pushing to master.

Similarly, if developing, you can set `DEPLOYMENT_MODE="dev"` under a service's environment variables in `./docker-compose.yaml` to get more debugging information.  Please toggle this to `DEPLOYMENT_MODE="prod"` when you are pushing to master.  

These configs are mainly for deployment so it won't matter much in this repo, but it's easier if we guarantee that those are toggled to production mode.  It's one simple check before each PR (can we do this in CI somehow?).

### Prerequisities

- [Docker](https://docs.docker.com/install/#supported-platforms)

### Testing

```bash
pytest ./services
```

### Precommit

In addition to running the tests, run linters.

```bash
pylint ./services
```
