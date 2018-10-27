"""API resources for the mentors table."""
import logging

from webargs import fields
from webargs.flaskparser import use_kwargs
from flask_restful import abort, Resource

from registration.src.api.utils import (
    is_valid_email, whitelist, WHITELIST_GIDS
)
from registration.src.db import DB, query_response_to_dict
from registration.src.models.mentor import Mentor

LOG = logging.getLogger(__name__)


class MentorRegistration(Resource):
    # pylint: disable=no-member,unused-argument,too-many-arguments,too-many-locals,no-self-use
    """Endpoints for registering a user or retrieving registered user(s)."""
    @use_kwargs({
        'uid': fields.String(required=True),
        'token': fields.String(required=True),
        'email': fields.String(missing=None),
    })
    @whitelist({WHITELIST_GIDS['dev']})
    def get(self, uid, token, email):
        """Gets a user's entry by their email.

        :param uid: UID to authenticate as
        :type  uid: string
        :param token: token (really a password) for the given UID
        :type  token: string
        :param email: [OPTIONAL] email to query for
        :type  email: string
        :returns: If an email is given, returns a list containing that one result
                  (because email is unique).  If there is no email in the
                  request, returns all users.
        :rtype: list of dicts
        :aborts: 400: email is given but with invalid format
                 404: email is not found in the DB
                 422: missing required parameter(s)
        """
        if email is not None and not is_valid_email(email):
            abort(400, message='Invalid email format')
        query = Mentor.query
        resp = query.all() if email is None else [query.filter_by(email=email).first_or_404()]
        return [query_response_to_dict(r) for r in resp]

    @use_kwargs({
        'uid': fields.String(required=True),
        'token': fields.String(required=True),
        'email': fields.String(required=True),
        'first_name': fields.String(required=True),
        'last_name': fields.String(required=True),
        'company': fields.String(required=True),
        'shirt_size': fields.String(required=True),
        'short_answer': fields.String(required=True),
        'mentor_field': fields.String(required=True),
        'github': fields.String(missing=None),
        'linkedin': fields.String(missing=None),
        'dietary_rest': fields.String(missing=None)
    })
    @whitelist({WHITELIST_GIDS['dev']})
    def post(self, uid, token, email, first_name, last_name, company, shirt_size,
             short_answer, mentor_field, github, linkedin, dietary_rest):
        """Inserts the user in the mentors table.
        Since this hooks into the DB, each field has specific constraints.
        Please check registration.src.models.mentor for more information.

        [OPTIONAL] tags indicate that the parameter was not in the request.
        For example, they do not indicate fields like an 'undeclared' major being
        [OPTIONAL].  For the sake of the database, 'undeclared' is a valid major.

        :param uid: UID to authenticate as
        :type  uid: string
        :param token: token (really a password) for the given UID
        :type  token: string
        :param email: user's email (UNIQUE for the DB)
        :type  email: string
        :param first_name: user's first name
        :type  first_name: string
        :param last_name: user's last name
        :type  last_name: string
        :param company: user's company
        :type  company: string
        :param shirt_size: XS, S, M, ..., shirt size to take into consideration for orders
        :type  shirt_size: string
        :param short_answer: user's reponse to the short answer question
        :type  short_answer: string
        :param mentor_field: what the mentor wants to help in (e.g. React)
        :type  mentor_field: string
        :param github: [OPTIONAL] Github profile URL
        :type  github: string
        :param linkedin: [OPTIONAL] LinkedIn profile URL
        :type  linkedin: string
        :param dietary_rest: [OPTIONAL] user's dietary restrictions
        :type  dietary_rest: comma-delimited string (might need to change this
                             to a list of strings)
        :returns: representation of the row that was posted
        :rtype: string
        :aborts: 422: missing required parameter(s)
                 500: internal DB error, usually because input did not match the constraints
                      set by the DB.  Is the column the correct type?  Unique?  Can it be NULL?
        """
        row = Mentor(
            email, first_name, last_name, company, shirt_size, short_answer, mentor_field,
            github=github, linkedin=linkedin, dietary_rest=dietary_rest
        )
        DB.session.add(row)
        DB.session.commit()
        return repr(row)
