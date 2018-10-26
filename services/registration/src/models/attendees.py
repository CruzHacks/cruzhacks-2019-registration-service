"""Defines RDBMS table for Attendee model."""
from uuid import uuid4
from registration.src.db import DB

class Attendees(DB.Model):
    # pylint: disable=no-member, too-few-public-methods, too-many-instance-attributes
    """Table of a people's submitted registration info."""
    __tablename__ = 'attendees'


    # pylint: disable=duplicate-code

    # Set internally by us, not required for __init__().
    private_id = DB.Column('private_id', DB.String(36), primary_key=True, nullable=False)
    public_id = DB.Column('public_id', DB.Integer, unique=True, nullable=False)
    checked_in = DB.Column("checked_in", DB.Boolean, nullable=False)

    # NOT NULL
    email = DB.Column('email', DB.String(50), unique=True, nullable=False)
    first_name = DB.Column('first_name', DB.String(20), nullable=False)
    last_name = DB.Column('last_name', DB.String(20), nullable=False)
    birthday = DB.Column('birthday', DB.DateTime, nullable=False) # YYYY-MM-DD
    university = DB.Column('university', DB.String(50), nullable=False)
    grad_year = DB.Column('grad_year', DB.Integer, nullable=False)
    shirt_size = DB.Column('shirt_size', DB.String(5), nullable=False)
    short_answer1 = DB.Column("short_answer1", DB.String(500), nullable=False)
    short_answer2 = DB.Column("short_answer2", DB.String(500), nullable=False)

    # NULLables
    gender = DB.Column('gender', DB.String(1))
    ethnicity = DB.Column('ethnicity', DB.String(20))
    major = DB.Column('major', DB.String(20))
    dietary_rest = DB.Column("dietary_rest", DB.String(50))
    num_hacks = DB.Column("num_hacks", DB.Integer)
    linkedin = DB.Column("linkedin", DB.String(50))
    github = DB.Column("github", DB.String(50))
    workshop_ideas = DB.Column("workshop_ideas", DB.String(250))

    # pylint: disable=line-too-long, too-many-arguments, duplicate-code, too-many-locals
    def __init__(self, email, first_name, last_name, birthday, university, grad_year, shirt_size,
                 short_answer1, short_answer2, gender=None, ethnicity=None, major=None,
                 dietary_rest=None, num_hacks=None, linkedin=None, github=None, workshop_ideas=None):

        # Still need public ID and private ID, generate them from unique email
        guid = uuid4()
        self.private_id = str(guid)

        # guid.int is 128 bits.  Save some space since there won't be 2**128 applicants.
        self.public_id = guid.int % (2**16)
        self.checked_in = False

        # Args.
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        self.university = university
        self.grad_year = grad_year
        self.shirt_size = shirt_size
        self.short_answer1 = short_answer1
        self.short_answer2 = short_answer2

        # Kwargs.
        self.gender = gender
        self.ethnicity = ethnicity
        self.major = major
        self.dietary_rest = dietary_rest
        self.num_hacks = num_hacks
        self.linkedin = linkedin
        self.github = github
        self.workshop_ideas = workshop_ideas

    def __repr__(self):
        return "{ Attendee: email=%s, name=%s %s, university=%s }" % (
            self.email, self.first_name, self.last_name, self.university)
