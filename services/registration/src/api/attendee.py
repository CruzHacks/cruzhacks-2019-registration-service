"""API resources for the attendees table."""
import os

from webargs import fields
from webargs.flaskparser import use_kwargs
from flask_restful import abort, Resource

from registration.src.api import base
from registration.src.api.utils.whitelist import verify, GIDS
from registration.src.api.utils.parsing import strip_non_num
from registration.src.db import DB
from registration.src.models.attendee import Attendee

class AttendeeAddResume(Resource):
    # pylint: disable=no-member, unused-argument, too-many-arguments, too-many-locals, no-self-use
    """Endpoints for managing an attendee's resume."""
    @use_kwargs({
        'email': fields.String(required=True),
        'resume_uri': fields.String(required=True)
    })
    def put(self, email, resume_uri):
        """ Updates an attendees resume_uri in the database.

        :param email: email to query for
        :type  email: string
        :param resume_uri: URI to the user's resume.  Typically an S3 URL or path.
        :type  resume_uri: string
        """
        attendee = Attendee.query.filter_by(email=email).first()
        if attendee.resume_uri is not None:
            abort(403, message='resume already exists')
        attendee.resume_uri = resume_uri
        DB.session.commit()
        return {'status': 'success'}


class AttendeeResumeExists(Resource):
    # pylint: disable=no-member, unused-argument, too-many-arguments, too-many-locals, no-self-use, missing-docstring
    @use_kwargs({
        'email': base.SimilarKwargs.GET['email']
    })
    def get(self, email):
        """ Checks if a resume exists for some user.

        :param email: email to query for
        :type  email: string
        """
        attendee = Attendee.query.filter_by(email=email).first()
        if attendee is None:
            abort(404, message='user not found')
        return attendee.resume_uri is not None


class AttendeeIsRegistered(Resource):
    # pylint: disable=no-member, unused-argument, too-many-arguments, too-many-locals, no-self-use
    """Endpoints for checking if an attendee is registered already."""
    @use_kwargs({
        'email': base.SimilarKwargs.GET['email']
    })
    def get(self, email):
        """Gets an attendee by email and returns whether they exist or not.

        :param email: email to query for
        :type  email: string
        :returns: True if a registered attendee has the specified email.  Else False.
        :rtype: bool
        """
        return base.is_user_registered(Attendee, email)


class AttendeeRegistration(Resource):
    # pylint: disable=no-member, unused-argument, too-many-arguments, too-many-locals, no-self-use
    """Endpoints for registering a user or retrieving registered user(s)."""
    @use_kwargs(base.SimilarKwargs.GET)
    @verify({GIDS['dev']})
    def get(self, uid, token, email):
        """Gets a user's entry by the model and their email.
        Gets all users by the model if email is omitted.

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
                 401: invalid permissions (not on whitelist or not in a required role)
                 404: email is not found in the DB
                 422: missing required parameter(s)
        """
        return base.get_user(Attendee, email=email)

    @use_kwargs({
        **base.SimilarKwargs.POST,
        'age': fields.Int(required=True),
        'university': fields.String(required=True),
        'short_answer1': fields.String(required=True),
        'short_answer2': fields.String(required=True),
        'phone_number': fields.String(required=True),
        'gender': fields.String(missing=None),
        'ethnicity': fields.String(missing=None),
        'major': fields.String(missing=None),
        'num_hacks': fields.String(missing=None),
        'workshop_ideas': fields.String(missing=None),
        'grad_year': fields.Int(missing=None),
        'resume_uri': fields.String(missing=None)
    })
    def post(self, email, first_name, last_name, age, university, shirt_size, short_answer1,
             short_answer2, phone_number, gender, ethnicity, major, num_hacks, linkedin, github,
             dietary_rest, workshop_ideas, grad_year, resume_uri):
        """Inserts the user in the attendees table.
        Since this hooks into the DB, each field has specific constraints.
        Please check registration.src.models.attendee for more information.

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
        :param age: user's age in years
        :type  age: int
        :param university: university that the user is enrolled in
        :type  university: string
        :param shirt_size: XS, S, M, ..., shirt size to take into consideration for orders
        :type  shirt_size: string
        :param short_answer1: user's reponse to the first short answer question
        :type  short_answer1: string
        :param short_answer2: user's reponse to the second short answer question
        :type  short_answer2: string
        :param phone_number: user's phone number
        :type  phone_number: string
        :param gender: [OPTIONAL] user's gender, or agender, etc.
        :type  gender: character
        :param ethnicity: [OPTIONAL] user's ethnicity
        :type  ethnicity: string
        :param major: [OPTIONAL] user's expected major (or undeclared)
        :type  major: string
        :param num_hacks: [OPTIONAL] number of hackathons that the user has attended previously
        :type  num_hacks: string
        :param github: [OPTIONAL] Github profile URL
        :type  github: string
        :param linkedin: [OPTIONAL] LinkedIn profile URL
        :type  linkedin: string
        :param dietary_rest: [OPTIONAL] user's dietary restrictions
        :type  dietary_rest: comma-delimited string (might need to change this to a list of strings)
        :param workshop_ideas: [OPTIONAL] comments about workshops that the user would
                               like to see implemented
        :type  workshop_ideas: string
        :param grad_year: [OPTIONAL] user's expected year of graduation
        :type  grad_year: int
        :param resume_uri: [OPTIONAL] URI to the user's resume.  Typically an S3 URL or path.
        :type  resume_uri: string
        :returns: representation of the row that was posted
        :rtype: string
        :aborts: 401: invalid permissions (not on whitelist or not in a required role)
                 422: missing required parameter(s)
                 500: internal DB error, usually because input did not match the constraints
                      set by the DB.  Is the column the correct type?  Unique?  Can it be NULL?
        """
        attendee = Attendee(
            email, first_name, last_name, age, university, shirt_size,
            short_answer1, short_answer2, strip_non_num(phone_number),
            gender=gender, ethnicity=ethnicity, major=major, num_hacks=num_hacks, github=github,
            linkedin=linkedin, dietary_rest=dietary_rest, workshop_ideas=workshop_ideas,
            grad_year=grad_year, resume_uri=resume_uri
        )
        return base.apply(attendee, email, os.environ['MAILCHIMP_ATTENDEE_LIST'])
