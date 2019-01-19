"""Initializes and configures Flask APP, including DB and API endpoints."""
import os
import re

from flask import Flask
from flask_cors import CORS
from registration.src import DEPLOYMENT_MODE
from registration.src.db import DB
from registration.src.api import API
from registration.src.models.accounts import Dev, Director, Organizer, User

APP = Flask(__name__)

CRUZHACKS_DOMAIN_REGEX = re.compile(r'^https?://(www.)?cruzhacks.com/?$')


def getenv_bool(variable, default=None):
    """Gets an environment variable and tries to convert a string to a bool."""
    var = os.getenv(variable, default=default)
    if isinstance(var, bool):
        return var
    assert isinstance(var, str)
    return var.lower() in {"true", "t", "1", "yes"}


with APP.app_context():
    APP.config['ERROR_404_HELP'] = False

    # Set DB connection.  If not found, raises KeyError and exits.
    APP.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

    # Assume we're not in dev.
    APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = getenv_bool(
        'SQLALCHEMY_TRACK_MODIFICATIONS', False
    )
    APP.config['SQLALCHEMY_RECORD_QUERIES'] = getenv_bool('SQLALCHEMY_RECORD_QUERIES', False)
    APP.config['SQLALCHEMY_ECHO'] = getenv_bool('SQLALCHEMY_ECHO', False)

    DB.init_app(APP)
    API.init_app(APP)

    if DEPLOYMENT_MODE in {'dev', 'stg'}:
        CORS(APP)
    else:
        CORS(APP, origins=CRUZHACKS_DOMAIN_REGEX)

    # Set any dev deployment modes here.
    if DEPLOYMENT_MODE == 'dev':
        APP.logger.warning('You are in development mode')  # pylint: disable=no-member
        APP.logger.warning('Do not push code to master until out of development mode!') #pylint: disable=no-member
        APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        APP.config['SQLALCHEMY_RECORD_QUERIES'] = True
        APP.config['SQLALCHEMY_ECHO'] = True
        DB.drop_all()

    DB.create_all() # Create any tables if they do not exist.

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=os.environ.get('PORT', 8000), debug=True)
