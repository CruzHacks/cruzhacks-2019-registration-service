"""Defines RDBMS table for Mentor model."""
# pylint: disable=duplicate-code
from uuid import uuid4
from registration.src.db import DB

class Mentor(DB.Model):
   # pylint: disable=no-member, too-few-public-methods, too-many-instance-attributes
    """Table of a mentor's submitted info."""
    __tablename__ = 'mentors'

    private_id = DB.Column('private_id', DB.String(36), primary_key=True, nullable=False)
    public_id = DB.Column('public_id', DB.String(36), unique=True, nullable=False)
    checked_in = DB.Column('checked_in', DB.Boolean, nullable=False)

    email = DB.Column('email', DB.String(50), unique=True, nullable=False)
    first_name = DB.Column('first_name', DB.String(30), nullable=False)
    last_name = DB.Column('last_name', DB.String(30), nullable=False)
    company = DB.Column('company', DB.String(50), nullable=False)
    shirt_size = DB.Column('shirt_size', DB.String(5), nullable=False)
    short_answer = DB.Column('short_answer', DB.String(500), nullable=False)
    mentor_field = DB.Column('mentor_field', DB.String(128), nullable=False)

    github = DB.Column('github', DB.String(80), nullable=True)
    linkedin = DB.Column('linkedin', DB.String(80), nullable=True)
    dietary_rest = DB.Column('dietary_rest', DB.String(50), nullable=True)

    is_accepted = DB.Column('is_accepted', DB.Boolean)

    # pylint: disable=too-many-arguments
    def __init__(self, email, first_name, last_name, company, shirt_size, short_answer,
                 mentor_field, github=None, linkedin=None, dietary_rest=None):

        self.private_id = str(uuid4())
        self.public_id = str(uuid4())
        self.checked_in = False

        # Args.
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.company = company
        self.shirt_size = shirt_size
        self.short_answer = short_answer
        self.mentor_field = mentor_field

        # Kwargs.
        self.github = github
        self.linkedin = linkedin
        self.dietary_rest = dietary_rest

        self.is_accepted = None

    def __repr__(self):
        return "{ Mentor: email=%s, name=%s %s, company=%s }" % (
            self.email, self.first_name, self.last_name, self.company)
