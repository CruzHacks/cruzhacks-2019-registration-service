"""Utilities for handling mailing lists."""
import os
import requests


def add(email, mailchimp_list_id):
    """Adds an email to the specified mailing list.

    :param email: email to add
    :type  email: string
    :param mailchimp_list_id: mailing list ID to add the email to
    :type  mailchimp_list_id: string
    :returns: JSON object with response.
    """
    url = 'https://us17.api.mailchimp.com/3.0/lists/' + mailchimp_list_id + '/members'
    return requests.post(
        url,
        json={'email_address': email, 'status': 'subscribed'},
        auth=('user', os.environ['MAILCHIMP_APIK'])
    )
