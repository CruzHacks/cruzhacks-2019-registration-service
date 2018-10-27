"""Defines RDBMS tables."""
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


def query_response_to_dict(response):
    """Converts a row from the DB into a dictionary (for jsonify preprocessing)."""
    resp = {}
    for column in response.__table__.columns.keys():
        value = getattr(response, column)
        if isinstance(value, datetime):
            date = value.__str__().split()[0]
            resp[column] = date
        else:
            resp[column] = value
    return resp


def get_query_res(table, **kwargs):
    """ Returns all kwarg matches in DB model as a list """
    return table.query.filter_by(**kwargs).all()
