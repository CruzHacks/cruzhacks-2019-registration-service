"""Defines RDBMS table for user model."""
from uuid import uuid4
from flask_sqlalchemy import SQLAlchemy
DB = SQLAlchemy()

class Judge(DB.model):
    # pylint: disable=no-member, too-few-public-methods, too-many-instance-attributes
    """Table of a judge's submitted info."""
    __tablename__ = 'judges'

    # required fields
    private_id = DB.Column('private_id', DB.String(36), primary_key=True, nullable=False)
    public_id = DB.Column('public_id', DB.Integer, unique=True, nullable=False)
    first_name = DB.Column('first_name', DB.String(20), nullable=False)
    last_name = DB.Column('last_name', DB.String(20), nullable=False)
    email = DB.Column('email', DB.String(50), unique=True, nullable=False)
    company = DB.Column('company', DB.String(50), nullable=False)
    short_answer1 = DB.Column('short_answer1', DB.String(500), nullable=False)
    short_answer2 = DB.Column('short_answer2', DB.String(500), nullable=False)
    size = DB.Column('t-shirt_size', DB.String(5), nullable=False)

    # optional fields
    optional_info = {}

    optional_info['github'] = DB.Column("github", DB.String(50), nullable=True)
    optional_info['linkedin'] = DB.Column("linkedin", DB.String(50), nullable=True)
    optional_info["dietary_rest"] = DB.Column("dietary_rest", DB.String(50), nullable=True)

    # pylint: disable=line-too-long, too-many-arguments
    def __init__(self, email, first_name, last_name, size, short_answer1, short_answer2, company, **kwargs):

        # Still need public ID and private ID, generate them from unique email
        guid = uuid4()
        self.private_id = str(guid)

        # guid.int is 128 bits.  Save some space since there won't be 2**128 applicants.
        self.public_id = guid.int % (2**16)

        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.size = size
        self.short_answer = short_answer
        self.company = company
        self.mentor_field = mentor_field

        for key, value in kwargs.items():
            self.optional_info[str(key)] = str(value)
   
    def __repr__(self):
        return "{ Judge: email=%s, name=%s %s, company=%s }" % (
            self.email, self.first_name, self.last_name, self.company)