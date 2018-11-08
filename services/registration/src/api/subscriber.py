"""API resources for general mailing list subscribers."""
import os

from webargs.flaskparser import use_kwargs
from flask_restful import Resource

from registration.src.api import base
from registration.src.api.utils import mailing_list


class SubscriberList(Resource):
    # pylint: disable=no-member, no-self-use
    """Endpoint to add to a generic email list."""
    @use_kwargs({
        'email': base.SimilarKwargs.POST['email']
    })
    def post(self, email):
        """Sends confirmation in a post req

        :param email: email to send to
        :type  email: String
        :returns: email success or error
        : rtype : String
        """
        return mailing_list.add(email, os.environ['MAILCHIMP_SUBSCRIBER_LIST'])
