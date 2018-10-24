"""Defines RDBMS table for user model."""
from uuid import uuid4
from flask_sqlalchemy import SQLAlchemy
DB = SQLAlchemy()

class Attendee(DB.Model):
    # pylint: disable=no-member, too-few-public-methods, too-many-instance-attributes
    """Table of a people's submitted registration info."""
    __tablename__ = 'registrations'

    # required fields
    # pylint: disable=duplicate-code
    private_id = DB.Column('private_id', DB.String(36), primary_key=True, nullable=False)
    public_id = DB.Column('public_id', DB.Integer, unique=True, nullable=False)
    email = DB.Column('email', DB.String(50), unique=True, nullable=False)
    first_name = DB.Column('first_name', DB.String(20), nullable=False)
    last_name = DB.Column('last_name', DB.String(20), nullable=False)
    birthday = DB.Column('birthday', DB.String(10), nullable=False) # MM-DD-YYYY
    university = DB.Column('school', DB.String(50), nullable=False)
    school_year = DB.Column('school_year', DB.Integer, nullable=False)
    size = DB.Column('t-shirt_size', DB.String(5), nullable=False)
    short_answer1 = DB.Column("short_answer1", DB.String(500), nullable=False)
    short_answer2 = DB.Column("short_answer2", DB.String(500), nullable=False)
    checkedin = DB.Column("checked_in", DB.Boolean, nullable=False)

    # optional fields
    optional_info = {}

    # M or F or O (other or prefer not to say?)
    optional_info["gender"] = DB.Column('gender', DB.String(1), nullable=True)
    optional_info["ethnicity"] = DB.Column('ethnicity', DB.String(20), nullable=True)
    optional_info["major"] = DB.Column('major', DB.String(20), nullable=True)
    optional_info["dietary_rest"] = DB.Column("dietary_rest", DB.String(50), nullable=True)
    optional_info["num_hacks"] = DB.Column("num_hacks", DB.Integer, nullable=True)
    optional_info["linkedin"] = DB.Column("linkedin", DB.String(50), nullable=True)
    optional_info["github"] = DB.Column("github", DB.String(50), nullable=True)

    # pylint: disable=line-too-long, too-many-arguments, duplicate-code
    def __init__(self, email, firstName, lastName, university, birthday, size, school_year, short_answer1, short_answer2, **kwargs):

        # Still need public ID and private ID, generate them from unique email
        guid = uuid4()
        self.private_id = str(guid)

        # guid.int is 128 bits.  Save some space since there won't be 2**128 applicants.
        self.public_id = guid.int % (2**16)
        self.checkedin = False

        # general info
        self.email = email
        self.first_name = firstName
        self.last_name = lastName
        self.university = university
        self.birthday = birthday
        self.size = size
        self.school_year = school_year
        self.short_answer1 = short_answer1
        self.short_answer2 = short_answer2

        for key, value in kwargs.items():
            self.optional_info[str(key)] = str(value)


    def __repr__(self):
        return "{ Attendee: email=%s, name=%s %s, school=%s }" % (
            self.email, self.first_name, self.last_name, self.school)
