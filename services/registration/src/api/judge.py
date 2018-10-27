"""API resources for the judges table."""
from webargs import fields
from webargs.flaskparser import use_kwargs
from flask_restful import Resource

from registration.src.api import base
from registration.src.api.utils.whitelist import verify, GIDS
from registration.src.models.judge import Judge


class JudgeRegistration(Resource):
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
        return base.get_user(Judge, email)

    @use_kwargs({
        **base.SimilarKwargs.POST,
        'company': fields.String(required=True),
        'short_answer1': fields.String(required=True),
        'short_answer2': fields.String(required=True),
    })
    @verify({GIDS['dev']})
    def post(self, uid, token, email, first_name, last_name, company, shirt_size,
             short_answer1, short_answer2, github, linkedin, dietary_rest):
        """Inserts the user in the judges table.
        Since this hooks into the DB, each field has specific constraints.
        Please check registration.src.models.judge for more information.

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
        :param short_answer1: user's reponse to the first short answer question
        :type  short_answer1: string
        :param short_answer2: user's reponse to the second short answer question
        :type  short_answer2: string
        :param github: [OPTIONAL] Github profile URL
        :type  github: string
        :param linkedin: [OPTIONAL] LinkedIn profile URL
        :type  linkedin: string
        :param dietary_rest: [OPTIONAL] user's dietary restrictions
        :type  dietary_rest: comma-delimited string (might need to change this
                             to a list of strings)
        :returns: representation of the row that was posted
        :rtype: string
        :aborts: 401: invalid permissions (not on whitelist or not in a required role)
                 422: missing required parameter(s)
                 500: internal DB error, usually because input did not match the constraints
                      set by the DB.  Is the column the correct type?  Unique?  Can it be NULL?
        """
        judge = Judge(
            email, first_name, last_name, company, shirt_size, short_answer1, short_answer2,
            github=github, linkedin=linkedin, dietary_rest=dietary_rest
        )
        return base.commit_user(judge)
