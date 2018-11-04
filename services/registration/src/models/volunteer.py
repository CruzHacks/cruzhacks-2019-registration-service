"""Defines RDBMS table for Volunteer model."""
# pylint: disable=duplicate-code
from uuid import uuid4
from registration.src.db import DB

class Volunteer(DB.Model):
   # pylint: disable=no-member, too-few-public-methods, too-many-instance-attributes
    """Table of a volunteer's submitted info."""
    __tablename__ = 'volunteers'

    # required fields
    private_id = DB.Column('private_id', DB.String(36), primary_key=True, nullable=False)
    public_id = DB.Column('public_id', DB.String(36), unique=True, nullable=False)
    checked_in = DB.Column('checked_in', DB.Boolean, nullable=False)

    # NON NULLABLE
    email = DB.Column('email', DB.String(50), unique=True, nullable=False)
    first_name = DB.Column('first_name', DB.String(30), nullable=False)
    last_name = DB.Column('last_name', DB.String(30), nullable=False)
    age = DB.Column('age', DB.Integer, nullable=False)
    shirt_size = DB.Column('shirt_size', DB.String(5), nullable=False)
    short_answer = DB.Column("short_answer", DB.String(500), nullable=False)
    assoc_clubs = DB.Column("assoc_clubs", DB.String(150), nullable=False)
    availability = DB.Column(DB.String(100), nullable=False)

    # NULLABLE
    github = DB.Column("github", DB.String(80))
    linkedin = DB.Column("linkedin", DB.String(80))
    dietary_rest = DB.Column("dietary_rest", DB.String(50))

    # pylint: disable=too-many-arguments
    def __init__(self, email, first_name, last_name, age, shirt_size, short_answer,
                 assoc_clubs, availability, github=None, linkedin=None, dietary_rest=None):

        self.private_id = str(uuid4())
        self.public_id = str(uuid4())
        self.checked_in = False

        # Args.
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.shirt_size = shirt_size
        self.short_answer = short_answer
        self.assoc_clubs = assoc_clubs
        self.availability = availability

        # Kwargs.
        self.github = github
        self.linkedin = linkedin
        self.dietary_rest = dietary_rest

    def __repr__(self):
        return "{ Volunteer: email=%s, name=%s %s }" % (
            self.email, self.first_name, self.last_name)
