"""API resources for the mailing list table."""
from webargs import fields
from webargs.flaskparser import use_kwargs
from flask_restful import Resource

from registration.src.api import base
from registration.src.api.utils.whitelist import verify, GIDS, FIELDS as whitelist_fields
from registration.src.models.mailing_list import MailingList
from registration.src.db import query_response_to_dict


class MailingListSubmit(Resource):
    # pylint: disable=no-member, unused-argument, too-many-arguments, too-many-locals, no-self-use
    """Endpoints for adding an email to the mailing list."""
    @use_kwargs(whitelist_fields)
    @verify({GIDS['dev']})
    def get(self, uid, token):
        """Returns all emails in the mailing list.

        :param uid: UID to authenticate as
        :type  uid: string
        :param token: token (really a password) for the given UID
        :type  token: string
        :aborts: 401: invalid permissions (not on whitelist or not in a required role)
                 422: missing required parameter(s)
        """
        return [query_response_to_dict(r)['email'] for r in MailingList.query.all()]

    @use_kwargs({
        'email': fields.String(required=True)
    })
    def post(self, email):
        """Adds an email to the mailing list.
        This doesn't return anything.  Inspect the HTTP status code instead.

        If the email already exists, do nothing.

        :param email: email to add
        :type  email: string
        :aborts: 400: email is given but with invalid format
                 422: missing required parameter(s)
        """
        if not base.is_user_registered(MailingList, email):
            email = MailingList(email)
            base.commit_user(email)
