"""Defines RDBMS table for Volunteer model."""
from uuid import uuid4
from registration.src.db import DB

class Volunteer(DB.Model):
   # pylint: disable=no-member, too-few-public-methods, too-many-instance-attributes
    """Table of a volunteer's submitted info."""
    __tablename__ = 'volunteers'

    # required fields
    # pylint: disable=duplicate-code
    private_id = DB.Column('private_id', DB.String(36), primary_key=True, nullable=False)
    public_id = DB.Column('public_id', DB.Integer, unique=True, nullable=False)
    checked_in = DB.Column('checked_in', DB.Boolean, nullable=False)

    # NON NULLABLE
    email = DB.Column('email', DB.String(50), unique=True, nullable=False)
    birthday = DB.Column('birthday', DB.String(10), nullable=False) # MM-DD-YYYY
    first_name = DB.Column('first_name', DB.String(20), nullable=False)
    last_name = DB.Column('last_name', DB.String(20), nullable=False)
    size = DB.Column('t-shirt_size', DB.String(5), nullable=False)
    short_answer = DB.Column("short_answer", DB.String(500), nullable=False)
    assoc_clubs = DB.Column("clubs", DB.String(150), nullable=False)
    availability = DB.Column(DB.String(100), nullable=False)

    # NULLABLE
    github = DB.Column("github", DB.String(50), nullable=True)
    linkedin = DB.Column("linkedin", DB.String(50), nullable=True)
    dietary_rest = DB.Column("dietary_rest", DB.String(50), nullable=True)

    # pylint: disable=line-too-long, too-many-arguments, duplicate-code
    def __init__(self, email, first_name, last_name, birthday, size, short_answer, assoc_clubs, availability,
                 github=None, linkedin=None, dietary_rest=None):

        # Still need public ID and private ID, generate them from unique email
        # pylint: disable=duplicate-code
        guid = uuid4()
        self.private_id = str(guid)

        # guid.int is 128 bits.  Save some space since there won't be 2**128 applicants.
        self.public_id = guid.int % (2**16)
        self.checked_in = False

        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        self.size = size
        self.short_answer = short_answer
        self.assoc_clubs = assoc_clubs
        self.availability = availability

        self.github = github
        self.linkedin = linkedin
        self.dietary_rest = dietary_rest

    def __repr__(self):
        return "{ Volunteer: email=%s, name=%s %s, school=%s }" % (
            self.email, self.first_name, self.last_name, self.school)
