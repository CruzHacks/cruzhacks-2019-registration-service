"""Utility functions for handling API requests."""
from datetime import datetime
from functools import wraps
import os

import bcrypt
from flask_restful import abort

from registration.src import IS_WHITELIST_ENABLED

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
                    hashed_input = bcrypt.hashpw(token, salt)  # pylint: disable=no-member
                    assert bcrypt.hashpw(token, hashed_input) == os.environ['{}_hashed'.format(uid)] # pylint: disable=no-member
                except (AssertionError, KeyError):
                    abort(401, message='Unauthorized access.  This incident will be reported.')
            return func(*args, **kwargs)
        return wrapper
    return decorator

def is_valid_email(email):
    """
    Ensures an email has a very basic, possibly correct format.

    An email may have invalid characters or an invalid domain,
    but that will be found when the user does not confirm an email.
    """
    try:
        split = email.split('@')
        assert len(split) == 2
        domain = split[1]
        assert '.' in domain
    except AssertionError:
        return False
    return True

def datestring_to_datetime(datestring):
    """Converts a date (as a string) to a datetime object.

    :param datestring: date in the format of 'yyyy-mm-dd'
    :type  datestring: string
    :rtype: datetime
    """
    return datetime(*[int(s) for s in datestring.split('-')])
