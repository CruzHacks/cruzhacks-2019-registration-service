"""Defines API helpers for all registration types."""
from webargs import fields
from flask_restful import abort

from registration.src.api.utils.parsing import is_valid_email
from registration.src.api.utils import whitelist
from registration.src.db import DB, query_response_to_dict


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


def get_user(model, email):
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


def commit_user(user):
    """Adds and commits a user as a row to the database.

    :param user: row to add into its table
    :type  user: instance of Flask-SQLAlchemy's db.model (like Attendee(), Judge(), etc.)
    :return: representation of the user
    :rtype: string
    :aborts: 500: internal DB error, usually because input did not match the constraints
                 set by the DB.  Is the column the correct type?  Unique?  Can it be NULL?
    """
    # pylint: disable=no-member,too-few-public-methods
    DB.session.add(user)
    DB.session.commit()
    return repr(user)
