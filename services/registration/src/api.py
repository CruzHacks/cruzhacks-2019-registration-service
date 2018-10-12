"""Defines API endpoints."""
#pylint: disable=unused-argument,invalid-name,no-member,no-self-use
import os
import logging
from functools import wraps

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
            uid = kwargs['uid']
            token = kwargs['token']
            try:
                assert os.environ['{}_token'.format(uid)] == token
            except (AssertionError, KeyError) as e:
                LOG.exception(e, 'Invalid request as uid={} and token={}'.format(uid, token))
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
        return [query_response_to_dict(r) for r in Attendee.query.all()]

    @use_kwargs({
        'uid': fields.String(required=True),
        'token': fields.String(required=True)
    })
    @whitelist
    def post(self, uid=None, token=None):
        """Creates a row in Registrations table."""
        DB.session.add(Attendee())
        DB.session.commit()
        return 'posted!'
