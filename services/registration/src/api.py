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
from registration.src.db import DB, query_response_to_dict
from registration.models.attendee import Attendee

API = Api()
LOG = logging.getLogger(__name__)

WHITELIST_GIDS = {
    'admin': 0,
    'dev': 1,
    'team': 2,
    'judge': 3,
    'mentor': 4
}


def whitelist(gids):
    """Decorator to verify whitelisted users before continuing.

    :param gids: Group IDs that can access the wrapped function.
    :type gids: set
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if IS_WHITELIST_ENABLED:
                try:
                    uid = kwargs['uid']

                    # Ensure that the user has at least one matching gid.
                    groups = os.environ['{}_groups'.format(uid)].split(',')
                    assert not gids.isdisjoint({WHITELIST_GIDS[g] for g in groups})

                    token = kwargs['token']
                    salt = os.environ['{}_salt'.format(uid)]
                    hashed_input = bcrypt.hashpw(token, salt)
                    assert bcrypt.hashpw(token, hashed_input) == os.environ['{}_hashed'.format(uid)]
                except (AssertionError, KeyError):
                    abort(401, message='Unauthorized access.  This incident will be reported.')
            return func(*args, **kwargs)
        return wrapper
    return decorator


@API.resource('/')
class Home(Resource):
    #pylint: disable=missing-docstring

    @use_kwargs({
        'uid': fields.String(required=True),
        'token': fields.String(required=True)
    })
    @whitelist({WHITELIST_GIDS['dev']})
    def get(self, uid=None, token=None):
        return "You're on the API whitelist!"


@API.resource('/register')
class Register(Resource):
    """Test endpoint for getting/posting users from the DB."""

    @use_kwargs({
        'uid': fields.String(required=True),
        'token': fields.String(required=True)
    })
    @whitelist({WHITELIST_GIDS['dev']})
    def get(self, uid=None, token=None):
        """Gets every row in Registrations table."""
        return [query_response_to_dict(r) for r in Attendee.query.all()]

    @use_kwargs({
        'uid': fields.String(required=True),
        'token': fields.String(required=True)
    })
    @whitelist({WHITELIST_GIDS['dev']})
    def post(self, uid=None, token=None):
        """Creates a row in Registrations table."""
        # pylint: disable=no-value-for-parameter
        DB.session.add(Attendee())
        DB.session.commit()
        return 'posted!'
