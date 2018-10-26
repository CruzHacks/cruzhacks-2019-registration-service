"""API resources for the Attendees table."""
import logging

from webargs import fields
from webargs.flaskparser import use_kwargs
from flask_restful import abort, Resource

from registration.src.api.utils import (
    datestring_to_datetime, is_valid_email, whitelist, WHITELIST_GIDS
)
from registration.src.db import DB, query_response_to_dict
from registration.src.models.attendees import Attendees

LOG = logging.getLogger(__name__)


class Register(Resource):
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
        """
        if email is not None and not is_valid_email(email):
            abort(400, message='Invalid email format')
        query = Attendees.query
        resp = query.all() if email is None else [query.filter_by(email=email).first_or_404()]
        return [query_response_to_dict(r) for r in resp]

    @use_kwargs({
        'uid': fields.String(required=True),
        'token': fields.String(required=True),
        'email': fields.String(required=True),
        'first_name': fields.String(required=True),
        'last_name': fields.String(required=True),
        'birthday': fields.String(required=True),
        'university': fields.String(required=True),
        'grad_year': fields.Int(required=True),
        'shirt_size': fields.String(required=True),
        'short_answer1': fields.String(required=True),
        'short_answer2': fields.String(required=True),
        'gender': fields.String(missing=None),
        'ethnicity': fields.String(missing=None),
        'major': fields.String(missing=None),
        'dietary_rest': fields.String(missing=None),
        'num_hacks': fields.String(missing=None),
        'linkedin': fields.String(missing=None),
        'github': fields.String(missing=None),
        'workshop_ideas': fields.String(missing=None)
    })
    @whitelist({WHITELIST_GIDS['dev']})
    def post(self, uid, token, email, first_name, last_name, birthday,
             university, grad_year, shirt_size, short_answer1, short_answer2,
             gender, ethnicity, major, dietary_rest, num_hacks, linkedin, github, workshop_ideas):
        """Inserts the user in the Attendees table.
        Since this hooks into the DB (Attendees), each field has specific constraints.
        Please check registration.src.models.attendees for more information.

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
        :param birthday: date of birth in the form YYYY-MM-DD
        :type  birthday: string
        :param university: university that the user is enrolled in
        :type  university: string
        :param grad_year: user's expected year of graduation
        :type  grad_year: int
        :param shirt_size: XS, S, M, ..., shirt size to take into consideration for orders
        :type  shirt_size: string
        :param short_answer1: user's reponse to the first short answer question
        :type  short_answer1: string
        :param short_answer2: user's reponse to the second short answer question
        :type  short_answer2: string
        :param gender: [OPTIONAL] user's gender, or agender, etc.
        :type  gender: character
        :param ethnicity: [OPTIONAL] user's ethnicity
        :type  ethnicity: string
        :param major: [OPTIONAL] user's expected major (or undeclared)
        :type  major: string
        :param dietary_rest: [OPTIONAL] user's dietary restrictions
        :type  dietary_rest: comma-delimited string (might need to change this to a list of strings)
        :param num_hacks: [OPTIONAL] number of hackathons that the user has attended previously
        :type  num_hacks: int
        :param linkedin: [OPTIONAL] LinkedIn profile URL
        :type  linkedin: string
        :param github: [OPTIONAL] Github profile URL
        :type  github: string
        :param workshop_ideas: [OPTIONAL] comments about workshops that the user would
                               like to see implemented
        :type  workshop_ideas: string
        """
        row = Attendees(
            email, first_name, last_name, datestring_to_datetime(birthday), university,
            grad_year, shirt_size, short_answer1, short_answer2,
            gender=gender, ethnicity=ethnicity, major=major, dietary_rest=dietary_rest,
            num_hacks=num_hacks, linkedin=linkedin, github=github, workshop_ideas=workshop_ideas
        )
        DB.session.add(row)
        DB.session.commit()
        return repr(row)
