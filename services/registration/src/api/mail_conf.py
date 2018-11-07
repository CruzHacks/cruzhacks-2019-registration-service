"""Sends confirmation email and adds users to email list"""
import os
# from flask import Flask, request, make_response, jsonify
import requests
from webargs import fields
from webargs.flaskparser import use_kwargs
from flask_restful import Resource

# APP = Flask(__name__)
class EmailConfirmation(Resource):
    # pylint: disable=no-member
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

        url = 'https://us17.api.mailchimp.com/3.0/lists/c566e13387/members'
        request_made = requests.post(url, json={'email_address':email, 'status':'subscribed'},
                                     auth=('user', os.environ['MAILCHIMP_APIK']))

        if request_made.status_code == 404:
            return "email error"

        return "email success"
