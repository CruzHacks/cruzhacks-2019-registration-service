"""API resources for the mailing list table."""
import os
import requests

from webargs import fields
from webargs.flaskparser import use_kwargs
from flask_restful import abort, Resource

from registration.src.api import base
from registration.src.api.utils.whitelist import verify, GIDS, FIELDS as whitelist_fields
from registration.src.models.mailing_list import MailingList
from registration.src.db import query_response_to_dict


def add(email, mailchimp_list_id):
    """Adds an email to the specified mailing list.

    :param email: email to add
    :type  email: string
    :param mailchimp_list_id: mailing list ID to add the email to
    :type  mailchimp_list_id: string
    :returns: JSON object with status attribute as subscribed.
    :aborts: anything mailchimp responds with as an error.
    """
    url = 'https://us17.api.mailchimp.com/3.0/lists/' + mailchimp_list_id + '/members'
    request_made = requests.post(url, json={'email_address': email, 'status': 'subscribed'},
                                 auth=('user', os.environ['MAILCHIMP_APIK']))
    response = request_made.json()

    if request_made.status_code < 200 or request_made.status_code > 299:
        abort(
            request_made.status_code,
            message='{}: {}'.format(response.get('title'), response.get('detail'))
        )

    return {'status': 'subscribed'}


class MailingListSubmit(Resource):
    # pylint: disable=no-member, unused-argument, too-many-arguments, too-many-locals, no-self-use
    """Endpoints for adding an email to the mailing list."""
    @use_kwargs({
        **whitelist_fields,
    })
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

class SubscriberListConfirmation(Resource):
    # pylint: disable=no-member, no-self-use, line-too-long
    """Endpoint to add to email list and send email confirmation."""

    @use_kwargs({
        'email': fields.String(required=True)
    })
    def post(self, email):
        """Sends confirmation in a post req
        :param email: email to send to
        :type  email: String

        :param api_key: api_key to access mailchimp
        :type  api_key: String

        :returns: email success or error
        : rtype : String
        """
        return add(email, str(os.environ['MAILCHIMP_SUBSCRIBER_LIST']))
