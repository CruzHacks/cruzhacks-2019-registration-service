# CruzHacks 2019 Backend Services

## Summary

This repo defines backend services for use within Docker.  Docker abstracts away your environment specific settings so that your code runs the same everywhere.  Each service's build environment is defined in a `Dockerfile`.  We bring up all of the services with `docker-compose.yaml`.

NGINX has been removed as a reverse proxy since we can use Heroku's router instead (and they offer more features for our already-deployed apps).  Using NGINX with the router is overkill and adds more latency.

## Getting Started

### Using the app

Each service is hosted on Heroku.  URLs are of the form `https://cruzhacks2019-SERVICENAME.herokuapp.com/`

#### Whitelist

APIs are secured with a whitelist of user/uid and pass/token request parameters.  PM a dev on the whitelist to be added.

You can check your access by (with your own uid and token):

```bash
curl -X GET https://cruzhacks2019-registration.herokuapp.com/?uid=fourloko&token=salvia
```

If you do not have access, you will receive this message:

```bash
{"message": "Unauthorized access.  This incident will be reported."}
```

Example with the registration service and the `register` endpoint:

```bash
curl -X GET https://cruzhacks2019-registration.herokuapp.com/register?uid=fourloko\&token=salvia
[{"private_id": "a2c41a62-4dd1-4d11-b8ad-c9d8a9a2525c", "public_id": 21084}, {"private_id": "fc0b90ee-2cdf-4788-a98a-99662facb85f", "public_id": 47199}]
```

### Local development

#### Building

Build containers for each service and run them:

(You shouldn't need to run with --build every time)

```bash
docker-compose up --build
```

This will build all images.  Postgres is locally built, but in prod, we use the Heroku Postgres add-on.

#### Storage

You can connect to the prod DB by copying the `DATABASE_URL` config var in Heroku and setting it as an environment variable in Docker.  Just make sure you only do reads.  If you want to do writes, copy the DB to a local instance and modify that instead.  Do not write to prod from your local instance unless there's a good reason.

Heroku also allows you to connect directly to the prod DB with psql if you need direct access.

#### API

Then hit your endpoints with the service's port.

In this example, the registration service is bound to port 8000:

```bash
curl -X POST localhost:8000/register?uid=fourloko\&token=balenciaga
curl -X GET localhost:8000/register?uid=fourloko\&token=balenciaga
curl -X GET localhost:8000/?uid=fourloko\&token=balenciaga
```

Replace GET with whatever HTTP verb you want to hit the endpoint with.  You may need the `--data` argument (for POSTs usually), check `man curl` for more details.

The port number varies depending on the service.  Verify that you're hitting the right port by checking for the service's container in `docker ps`. 

#### Config

To ease development, set `ENV GUNICORN_AUTO_RELOAD="on"` at the bottom of `./services/registration/Dockerfile`.  This will allow you to make changes in source code that is reflected on your running Docker container.  Please toggle this to `ENV GUNICORN_AUTO_RELOAD="off"` when you are pushing to master.

Similarly, if developing, you can set `DEPLOYMENT_MODE=dev` under a service's environment variables in `./docker-compose.yaml` to get more debugging information.  Please toggle this to `DEPLOYMENT_MODE=prod` when you are pushing to master.  

These configs are mainly for deployment so it won't matter much in this repo, but it's easier if we guarantee that those are toggled to production mode.  It's one simple check before each PR (can we do this in CI somehow?).

### Prerequisities

- [Docker](https://docs.docker.com/install/#supported-platforms)
- CircleCI: for MacOS on [Homebrew](https://brew.sh/), run `brew install circleci`

### Testing

```bash
circle build --job test
```

### Precommit

In addition to running the tests, run linters.

```bash
circle build --job lint
```
