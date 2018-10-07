"""Initializes and configures Flask APP, including DB and API endpoints."""
import os
from flask import Flask
<<<<<<< HEAD
from registration.models.attendee import DB
=======
from registration.src import DEPLOYMENT_MODE
from registration.src.db import DB
>>>>>>> b56c5cda2e251a024aceee945c4801549d8faff2
from registration.src.api import API

APP = Flask(__name__)

with APP.app_context():
    # Set DB connection.  If not found, raises KeyError and exits.
    APP.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

    # Assume we're not in dev.
    APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    APP.config['SQLALCHEMY_RECORD_QUERIES'] = False
    APP.config['SQLALCHEMY_ECHO'] = False

    DB.init_app(APP)
    API.init_app(APP)

    # Set any dev deployment modes here.
    if DEPLOYMENT_MODE == 'dev':
        APP.logger.warning('You are in development mode')
        APP.logger.warning('Do not push code to master until out of development mode!')
        APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        APP.config['SQLALCHEMY_RECORD_QUERIES'] = True
        APP.config['SQLALCHEMY_ECHO'] = True
        DB.drop_all()

    DB.create_all() # Create any tables if they do not exist.

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=os.environ.get('PORT', 8000), debug=True)
