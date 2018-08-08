"""Defines RDBMS table for user model."""
from uuid import uuid4
from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


def query_response_to_dict(response):
    """Converts a query response from the DB into a dictionary (for jsonify preprocessing)."""
    return dict((col, getattr(response, col)) for col in response.__table__.columns.keys())


def get_query_res(table, **kwargs):
    """ Returns all kwarg matches in DB model as a list """
    return table.query.filter_by(**kwargs).all()


class Attendee(DB.Model):
    #pylint: disable=no-member,too-few-public-methods
    """Table of a people's submitted registration info."""
    __tablename__ = 'registrations'

    private_id = DB.Column('private_id', DB.String(36), primary_key=True)
    public_id = DB.Column('public_id', DB.Integer, unique=True, nullable=False)
    email = DB.Column('email', DB.String(50), unique = True)
    first_name = DB.Column('first_name', DB.String(50))
    last_name = DB.Column('last_name', DB.String(50))
    school = DB.Column('school', DB.String(50))
    url = DB.Column('url', DB.String(100), nullable=True)

    # Fill in the other attributes from DBSchema.md

    def __init__(self, email='', fn='', ln='', univ=''):
        # Still need public ID and private ID, generate them from unique email
        guid = uuid4()
        self.private_id = str(guid)

        # guid.int is 128 bits.  Save some space since there won't be 2**128 applicants.
        self.public_id = guid.int % (2**16)

        # general info
        self.email = email
        self.first_name = fn
        self.last_name = ln
        self.school = univ

    def __repr__(self):
        return "{ Attendee: email=%s, name=%s %s, school=%s }" % (self.email, self.first_name, self.last_name, self.school)
