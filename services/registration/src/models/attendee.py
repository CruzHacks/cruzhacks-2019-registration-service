"""Defines RDBMS table for Attendee model."""
# pylint: disable=duplicate-code
from uuid import uuid4
from registration.src.db import DB

class Attendee(DB.Model):
    # pylint: disable=no-member, too-few-public-methods, too-many-instance-attributes
    """Table of a people's submitted registration info."""
    __tablename__ = 'attendees'

    # Set internally by us, not required for __init__().
    private_id = DB.Column('private_id', DB.String(36), primary_key=True, nullable=False)
    public_id = DB.Column('public_id', DB.String(36), unique=True, nullable=False)
    checked_in = DB.Column("checked_in", DB.Boolean, nullable=False)

    # NOT NULL
    email = DB.Column('email', DB.String(50), unique=True, nullable=False)
    first_name = DB.Column('first_name', DB.String(30), nullable=False)
    last_name = DB.Column('last_name', DB.String(30), nullable=False)
    phone_number = DB.Column('phone_number', DB.String(15), nullable=False)
    age = DB.Column('age', DB.Integer, nullable=False)
    university = DB.Column('university', DB.String(50), nullable=False)
    shirt_size = DB.Column('shirt_size', DB.String(5), nullable=False)
    short_answer1 = DB.Column("short_answer1", DB.String(500), nullable=False)
    short_answer2 = DB.Column("short_answer2", DB.String(500), nullable=False)

    # NULLables
    gender = DB.Column('gender', DB.String(25))
    ethnicity = DB.Column('ethnicity', DB.String(35))
    major = DB.Column('major', DB.String(100))
    num_hacks = DB.Column("num_hacks", DB.String(3))
    github = DB.Column("github", DB.String(80))
    linkedin = DB.Column("linkedin", DB.String(80))
    dietary_rest = DB.Column("dietary_rest", DB.String(50))
    workshop_ideas = DB.Column("workshop_ideas", DB.String(250))
    grad_year = DB.Column('grad_year', DB.Integer)
    resume_uri = DB.Column('resume_uri', DB.String(120))

    # pylint: disable=too-many-arguments, too-many-locals
    def __init__(self, email, first_name, last_name, age, university, shirt_size,
                 short_answer1, short_answer2, phone_number, gender=None, ethnicity=None,
                 major=None, num_hacks=None, github=None, linkedin=None, dietary_rest=None,
                 workshop_ideas=None, grad_year=None, resume_uri=None):

        self.private_id = str(uuid4())
        self.public_id = str(uuid4())
        self.checked_in = False

        # Args.
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.university = university
        self.shirt_size = shirt_size
        self.short_answer1 = short_answer1
        self.short_answer2 = short_answer2
        self.phone_number = phone_number

        # Kwargs.
        self.gender = gender
        self.ethnicity = ethnicity
        self.major = major
        self.num_hacks = num_hacks
        self.github = github
        self.linkedin = linkedin
        self.dietary_rest = dietary_rest
        self.workshop_ideas = workshop_ideas
        self.grad_year = grad_year
        self.resume_uri = resume_uri

    def __repr__(self):
        return "{ Attendee: email=%s, name=%s %s, university=%s }" % (
            self.email, self.first_name, self.last_name, self.university)
