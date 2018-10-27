"""Whitelisting and authorizing users."""
from functools import wraps
import os

import bcrypt
from flask_restful import abort
from webargs import fields

from registration.src import IS_WHITELIST_ENABLED

GIDS = {
    'admin': 0,
    'dev': 1,
    'team': 2,
    'judge': 3,
    'mentor': 4
}

FIELDS = {
    'uid': fields.String(required=True),  # pylint: disable=no-member
    'token': fields.String(required=True)  # pylint: disable=no-member
}

def verify(gids):
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
                    assert not gids.isdisjoint({GIDS[g] for g in groups})

                    token = kwargs['token']
                    salt = os.environ['{}_salt'.format(uid)]
                    hashed_input = bcrypt.hashpw(token, salt)  # pylint: disable=no-member
                    assert bcrypt.hashpw(token, hashed_input) == os.environ['{}_hashed'.format(uid)] # pylint: disable=no-member
                except (AssertionError, KeyError):
                    abort(401, message='Unauthorized access.  This incident will be reported.')
            return func(*args, **kwargs)
        return wrapper
    return decorator
