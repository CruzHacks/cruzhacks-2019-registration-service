"""Defines API endpoints."""
#pylint: disable=unused-argument,invalid-name,no-member,no-self-use
import os
import logging
from functools import wraps

import bcrypt
from webargs import fields
from webargs.flaskparser import use_kwargs
from flask_restful import abort, Api, Resource

from registration.src import IS_WHITELIST_ENABLED
from registration.src.db import DB, Registrations, query_response_to_dict

API = Api()
LOG = logging.getLogger(__name__)


def whitelist(func):
    """Decorator to verify whitelisted users before continuing."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if IS_WHITELIST_ENABLED:
            try:
                uid = kwargs['uid']
                token = kwargs['token']
                salt = os.environ['{}_salt'.format(uid)]
                hashed_input = bcrypt.hashpw(token, salt)
                assert bcrypt.hashpw(token, hashed_input) == os.environ['{}_hashed'.format(uid)]
            except (AssertionError, KeyError):
                abort(401, message='Unauthorized access.  This incident will be reported.')
        return func(*args, **kwargs)
    return wrapper


@API.resource('/')
class Home(Resource):
    #pylint: disable=missing-docstring

    @use_kwargs({
        'uid': fields.String(required=True),
        'token': fields.String(required=True)
    })
    @whitelist
    def get(self, uid=None, token=None):
        return "You're on the API whitelist!"


@API.resource('/register')
class Register(Resource):
    """Test endpoint for getting/posting users from the DB."""

    @use_kwargs({
        'uid': fields.String(required=True),
        'token': fields.String(required=True)
    })
    @whitelist
    def get(self, uid=None, token=None):
        """Gets every row in Registrations table."""
        return [query_response_to_dict(r) for r in Registrations.query.all()]

    @use_kwargs({
        'uid': fields.String(required=True),
        'token': fields.String(required=True)
    })
    @whitelist
    def post(self, uid=None, token=None):
        """Creates a row in Registrations table."""
        DB.session.add(Registrations())
        DB.session.commit()
        return 'posted!'
