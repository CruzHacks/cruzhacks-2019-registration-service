"""Whitelisting and authorizing users."""
from functools import wraps
import logging
import os

import bcrypt
from flask_restful import abort
from webargs import fields

from registration.src import IS_WHITELIST_ENABLED
from registration.src.models.accounts import Dev, Director, Organizer, User

FIELDS = {
    'uid': fields.String(required=True),  # pylint: disable=no-member
    'token': fields.String(required=True)  # pylint: disable=no-member
}

LOG = logging.getLogger(__name__)

def verify(group_models):
    """Decorator to verify whitelisted users before continuing.

    :param group_models: DB models of the groups that are required for access
    :type  group_models: set
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if IS_WHITELIST_ENABLED:
                try:
                    # Check that the user is valid.
                    uid = kwargs['uid']
                    token = kwargs['token'].encode('utf8')
                    user = User.query.get(uid)
                    assert bcrypt.checkpw(token, user.encrypted_password)

                    # Ensure that the user has permissions in some group.
                    matches = [True if g.query.get(uid) is not None else False for g in group_models]
                    assert any(matches)
                except (AssertionError, KeyError) as e:
                    abort(401, message='Unauthorized access.  This incident will be reported. {}'.format(e))
            return func(*args, **kwargs)
        return wrapper
    return decorator
