"""Defines RDBMS table for Judge model."""
from uuid import uuid4
from registration.src.db import DB

class Judge(DB.Model):
    # pylint: disable=no-member, too-few-public-methods, too-many-instance-attributes
    """Table of a judge's submitted info."""
    __tablename__ = 'judges'

    # pylint: disable=duplicate-code

    # set internally
    private_id = DB.Column('private_id', DB.String(36), primary_key=True, nullable=False)
    public_id = DB.Column('public_id', DB.Integer, unique=True, nullable=False)
    checked_in = DB.Column('checked_in', DB.Boolean, nullable=False)

    # NON NULLABLE
    first_name = DB.Column('first_name', DB.String(20), nullable=False)
    last_name = DB.Column('last_name', DB.String(20), nullable=False)
    email = DB.Column('email', DB.String(50), unique=True, nullable=False)
    company = DB.Column('company', DB.String(50), nullable=False)
    short_answer1 = DB.Column('short_answer1', DB.String(500), nullable=False)
    short_answer2 = DB.Column('short_answer2', DB.String(500), nullable=False)
    size = DB.Column('t-shirt_size', DB.String(5), nullable=False)

    # NULLABLE
    github = DB.Column("github", DB.String(50), nullable=True)
    linkedin = DB.Column("linkedin", DB.String(50), nullable=True)
    dietary_rest = DB.Column("dietary_rest", DB.String(50), nullable=True)

    # pylint: disable=line-too-long, too-many-arguments, duplicate-code
    def __init__(self, email, first_name, last_name, size, short_answer1, short_answer2, company,
                 github=None, linkedin=None, dietary_rest=None):

        # Still need public ID and private ID, generate them from unique email
        # pylint: disable=duplicate-code
        guid = uuid4()
        self.private_id = str(guid)
        # guid.int is 128 bits.  Save some space since there won't be 2**128 applicants.
        self.public_id = guid.int % (2**16)
        self.checked_in = False

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.size = size
        self.short_answer1 = short_answer1
        self.short_answer2 = short_answer2
        self.company = company

        self.github = github
        self.linkedin = linkedin
        self.dietary_rest = dietary_rest

    def __repr__(self):
        return "{ Judge: email=%s, name=%s %s, company=%s }" % (
            self.email, self.first_name, self.last_name, self.company)
