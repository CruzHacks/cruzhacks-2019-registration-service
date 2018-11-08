"""Utilities for handling mailing lists."""
import os
import requests

from flask_restful import abort


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
    request_made = requests.post(
        url,
        json={'email_address': email, 'status': 'subscribed'},
        auth=('user', os.environ['MAILCHIMP_APIK'])
    )
    response = request_made.json()

    request_did_error = request_made.status_code < 200 or request_made.status_code > 299
    if request_did_error:
        abort(
            request_made.status_code,
            status='failed',
            title=response.get('title'),
            detail=response.get('detail'),
            errors=response.get('errors')
        )

    return {'status': 'subscribed'}
