"""API resources for general mailing list subscribers."""
import logging
import os

from webargs.flaskparser import use_kwargs
from flask_restful import abort, Resource

from registration.src.api import base
from registration.src.api.utils import mailing_list

LOG = logging.getLogger(__name__)

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
        response = mailing_list.add(email, os.environ['MAILCHIMP_SUBSCRIBER_LIST'])
        jsoned_response = response.json()

        request_did_error = response.status_code < 200 or response.status_code > 299
        if request_did_error:
            LOG.error('Failed to add {} to mailing list: {}'.format(email, jsoned_response))
            abort(
                jsoned_response.get('status'),
                status='failed',
                title=jsoned_response.get('title'),
                detail=jsoned_response.get('detail'),
                errors=jsoned_response.get('errors')
            )
        return {'status': 'success'}
