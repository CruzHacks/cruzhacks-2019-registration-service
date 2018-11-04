# CruzHacks 2019 Backend Services

## Summary

This repo defines backend services for use within Docker.  Docker abstracts away your environment specific settings so that your code runs the same everywhere.  Each service's build environment is defined in a `Dockerfile`.  We bring up all of the services with `docker-compose.yaml`.

NGINX has been removed as a reverse proxy since we can use Heroku's router instead (and they offer more features for our already-deployed apps).  Using NGINX with the router is overkill and adds more latency.

## Getting Started

### Using the app

Each service is hosted on Heroku.  URLs are of the form `https://cruzhacks2019-SERVICENAME.herokuapp.com/`

#### Whitelist

APIs are secured with a whitelist of user/uid and pass/token request parameters.  PM a dev on the whitelist to be added.

There are also roles with access to different functions and endpoints, so make sure you're added to the right roles.

If you do not have access to an endpoint, you will receive this message:

```bash
{"message": "Unauthorized access.  This incident will be reported."}
```

For a full list of parameters, please see the [API parameters](services/registration/src/api/attendees.py) and its [schema](services/registration/src/models/attendees.py).

Examples with the registration service and the `register/attendee` endpoint:

```json
// Retrieve ALL users.  But we didn't add any yet!
curl -X GET localhost:8000/register/attendee?uid=foo\&token=salvia | jq '.'
[]

// Add user with unique email.
curl -H "Content-Type: application/json" -X POST -d '{"email": "amickey@ucsc.edu", "first_name": "Allston", "last_name": "Mickey", "age": 20, "university": "UCSC", "grad_year": 2019, "shirt_size": "M", "short_answer1": "sa1", "short_answer2": "sa2", "phone_number": "1234567890"}' localhost:8000/register/attendee
"{ Attendee: email=amickey@ucsc.edu, name=Allston Mickey, university=UCSC }"

// Retrieve ALL users.
curl -X GET localhost:8000/register/attendee?uid=foo\&token=salvia | jq '.'
[
  {
    "private_id": "70509e3e-1e52-4c3b-bf11-a89ba5145dfc",
    "public_id": "29c6a444-9308-44c0-a9da-04ce05cf3e03",
    "checked_in": false,
    "email": "amickey@ucsc.edu",
    "first_name": "Allston",
    "last_name": "Mickey",
    "phone_number": "1234567890",
    "age": 20,
    "university": "UCSC",
    "shirt_size": "M",
    "short_answer1": "sa1",
    "short_answer2": "sa2",
    "gender": null,
    "ethnicity": null,
    "major": null,
    "num_hacks": null,
    "github": null,
    "linkedin": null,
    "dietary_rest": null,
    "workshop_ideas": null,
    "grad_year": 2019,
    "resume_uri": null
  }
]

// Retrieve user by email.
curl -X GET localhost:8000/register/attendee?uid=foo\&token=salvia\&email=amickey@ucsc.edu | jq '.'
[
  {
    "private_id": "70509e3e-1e52-4c3b-bf11-a89ba5145dfc",
    "public_id": "29c6a444-9308-44c0-a9da-04ce05cf3e03",
    "checked_in": false,
    "email": "amickey@ucsc.edu",
    "first_name": "Allston",
    "last_name": "Mickey",
    "phone_number": "1234567890",
    "age": 20,
    "university": "UCSC",
    "shirt_size": "M",
    "short_answer1": "sa1",
    "short_answer2": "sa2",
    "gender": null,
    "ethnicity": null,
    "major": null,
    "num_hacks": null,
    "github": null,
    "linkedin": null,
    "dietary_rest": null,
    "workshop_ideas": null,
    "grad_year": 2019,
    "resume_uri": null
  }
]

// Add a second user.
curl -H "Content-Type: application/json" -X POST -d '{"email": "cruzhacks@ucsc.edu", "first_name": "Sammy", "last_name": "Slug", "age": 33, "university": "UCSC", "grad_year": 2020, "shirt_size": "XL", "short_answer1": "sa1", "short_answer2": "sa2", "phone_number": "0987654321", "dietary_rest": "salt"}' localhost:8000/register/attendee
"{ Attendee: email=cruzhacks@ucsc.edu, name=Sammy Slug, university=UCSC }"

// Retrieve ALL users.
curl -X GET localhost:8000/register/attendee?uid=foo\&token=salvia | jq '.'
[
  {
    "private_id": "70509e3e-1e52-4c3b-bf11-a89ba5145dfc",
    "public_id": "29c6a444-9308-44c0-a9da-04ce05cf3e03",
    "checked_in": false,
    "email": "amickey@ucsc.edu",
    "first_name": "Allston",
    "last_name": "Mickey",
    "phone_number": "1234567890",
    "age": 20,
    "university": "UCSC",
    "shirt_size": "M",
    "short_answer1": "sa1",
    "short_answer2": "sa2",
    "gender": null,
    "ethnicity": null,
    "major": null,
    "num_hacks": null,
    "github": null,
    "linkedin": null,
    "dietary_rest": null,
    "workshop_ideas": null,
    "grad_year": 2019,
    "resume_uri": null
  },
  {
    "private_id": "c5129b1e-bc34-4ceb-a237-742711aaf53d",
    "public_id": "b8c224e3-e4ce-447d-a57f-c7e4a89063ff",
    "checked_in": false,
    "email": "cruzhacks@ucsc.edu",
    "first_name": "Sammy",
    "last_name": "Slug",
    "phone_number": "0987654321",
    "age": 33,
    "university": "UCSC",
    "shirt_size": "XL",
    "short_answer1": "sa1",
    "short_answer2": "sa2",
    "gender": null,
    "ethnicity": null,
    "major": null,
    "num_hacks": null,
    "github": null,
    "linkedin": null,
    "dietary_rest": "salt",
    "workshop_ideas": null,
    "grad_year": 2020,
    "resume_uri": null
  }
]

// Retrieve user by email.
curl -X GET localhost:8000/register/attendee?uid=foo\&token=salvia\&email=cruzhacks@ucsc.edu | jq '.'
[
  {
    "private_id": "c5129b1e-bc34-4ceb-a237-742711aaf53d",
    "public_id": "b8c224e3-e4ce-447d-a57f-c7e4a89063ff",
    "checked_in": false,
    "email": "cruzhacks@ucsc.edu",
    "first_name": "Sammy",
    "last_name": "Slug",
    "phone_number": "0987654321",
    "age": 33,
    "university": "UCSC",
    "shirt_size": "XL",
    "short_answer1": "sa1",
    "short_answer2": "sa2",
    "gender": null,
    "ethnicity": null,
    "major": null,
    "num_hacks": null,
    "github": null,
    "linkedin": null,
    "dietary_rest": "salt",
    "workshop_ideas": null,
    "grad_year": 2020,
    "resume_uri": null
  }
]
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
