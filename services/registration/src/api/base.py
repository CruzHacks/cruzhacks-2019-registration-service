"""Defines API helpers for all registration types."""
import logging

from webargs import fields
from flask_restful import abort

from registration.src.api.utils import mailing_list
from registration.src.api.utils.parsing import is_valid_email
from registration.src.api.utils import whitelist
from registration.src.db import DB, query_response_to_dict

LOG = logging.getLogger(__name__)


class SimilarKwargs:
    """Namespacing for fields (for use_kwargs()) that are common between all models."""
    # pylint: disable=no-member,too-few-public-methods

    # Used in GET requests.
    GET = {
        **whitelist.FIELDS,
        'email': fields.String(missing=None)
    }

    # Used in POST requests.
    POST = {
        'email': fields.String(required=True),
        'first_name': fields.String(required=True),
        'last_name': fields.String(required=True),
        'shirt_size': fields.String(required=True),
        'linkedin': fields.String(missing=None),
        'github': fields.String(missing=None),
        'dietary_rest': fields.String(missing=None),
    }


def is_user_registered(model, email):
    """Checks if a user is registered on the specified email.

    :param model: the class of the model to use (the class itself, NOT instantiated)
    :type  model: class of Flask-SQLAlchemy's db.Model (like Attendee, Judge, etc.)
    :param email: email to query for
    :type  email: string
    :returns: If an entry with the email is found, return True.  Else return False.
    :rtype: bool
    :aborts: 400: email is given but with invalid format
    """
    if email is not None and not is_valid_email(email):
        abort(400, message='Invalid email format')
    return bool(model.query.filter_by(email=email).first())


def get_user(model, email=None):
    """Gets a user's entry by the model and their email.
    Gets all users by the model if email is omitted.

    :param model: the class of the model to use (the class itself, NOT instantiated)
    :type  model: class of Flask-SQLAlchemy's db.Model (like Attendee, Judge, etc.)
    :param email: [OPTIONAL] email to query for
    :type  email: string
    :returns: If an email is given, returns a list containing that one result
                (because email is unique).  If there is no email in the
                request, returns all users.
    :rtype: list of dicts
    :aborts: 400: email is given but with invalid format
             404: email is not found in the DB
    """
    if email is not None and not is_valid_email(email):
        abort(400, message='Invalid email format')
    query = model.query
    resp = query.all() if email is None else [query.filter_by(email=email).first_or_404()]
    return [query_response_to_dict(r) for r in resp]


def add_and_commit(row):
    """Adds and commits a user as a row to the database.

    :param row: row to add into its table
    :type  row: instance of Flask-SQLAlchemy's db.model (like Attendee(), Judge(), etc.)
    :return: representation of the user
    :rtype: string
    :aborts: 500: internal DB error, usually because input did not match the constraints
                 set by the DB.  Is the column the correct type?  Unique?  Can it be NULL?
    """
    # pylint: disable=no-member,too-few-public-methods
    DB.session.add(row)
    DB.session.commit()
    return repr(row)


def apply(user, email, mailchimp_list_id):
    # pylint: disable=no-member
    """Used for applying a user.
    Includes adding the user to the DB and to the respective mailing list.
    If anything fails, we rollback the DB.

    :param user: row to add into its table
    :type  user: instance of Flask-SQLAlchemy's db.model (like Attendee(), Judge(), etc.)
    :param email: email of the user to add to a mailing list
    :type  email: string
    :param mailchimp_list_id: mailing list ID to add the email to
    :type  mailchimp_list_id: string
    :returns: {'status': 'success'}
    :rtype: dict
    :aborts: on errors for DB commit or mailing list addition
    """
    try:
        add_and_commit(user)
    except Exception as e:  # pylint: disable=broad-except,invalid-name
        DB.session.rollback()
        LOG.exception(e)
        abort(500, message='Internal server error')

    response = mailing_list.add(email, mailchimp_list_id)
    jsoned_response = response.json()

    request_did_error = response.status_code < 200 or response.status_code > 299
    if request_did_error:
        LOG.error('Failed to add {} to mailing list: {}'.format(email, jsoned_response))  # pylint: disable=logging-format-interpolation
        DB.session.rollback()
        abort(
            jsoned_response.get('status'),
            status='failed',
            title=jsoned_response.get('title'),
            detail=jsoned_response.get('detail'),
            errors=jsoned_response.get('errors')
        )
    return {'status': 'success'}
