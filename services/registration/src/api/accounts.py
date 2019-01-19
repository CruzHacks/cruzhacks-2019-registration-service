"""API resources for managing announcements."""
import logging

from webargs import fields
from webargs.flaskparser import use_kwargs
from flask_restful import abort, Resource
import bcrypt

from registration.src.api.base import add_and_commit
from registration.src.api.utils.whitelist import GROUP_MODELS, user_exists_and_password_matches, verify
from registration.src.db import DB, query_response_to_dict
from registration.src.models.accounts import User as UserModel

LOG = logging.getLogger(__name__)

class User(Resource):
    # pylint: disable=no-member, unused-argument, too-many-arguments, too-many-locals, no-self-use
    """Endpoints for registering a user or retrieving registered user(s)."""
    @use_kwargs({
        'uid': fields.String(required=True),
        'token': fields.String(required=True)
    })
    def post(self, uid, token):
        """Creates an account without any roles.

        :param uid: UID to authenticate as
        :type  uid: string
        :param token: token (really a password) for the given UID
        :type  token: string
        """
        encrypted_password = bcrypt.hashpw(token.encode('utf8'), bcrypt.gensalt())
        u = UserModel(uid, encrypted_password)  # pylint: disable=invalid-name
        try:
            add_and_commit(u)
        except Exception as e:  # pylint: disable=broad-except,invalid-name
            DB.session.rollback()
            LOG.exception(e)
            abort(500, message='Internal server error')
        return {'status': 'success'}

class Verify(Resource):
    @use_kwargs({
        'uid': fields.String(required=True),
        'token': fields.String(required=True),
        'groups': fields.String(required=True)
    })
    def get(self, uid, token, groups):
        group_models = {GROUP_MODELS[g] for g in groups.split(',') if g and g in GROUP_MODELS}
        if user_exists_and_password_matches(uid, token.encode('utf8'), group_models):
            return {'status': 'success'}
        else:
            abort(401, message='Invalid username, password, or groups')
