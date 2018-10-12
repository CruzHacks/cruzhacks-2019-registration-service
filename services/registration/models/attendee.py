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

    # required fields
    private_id = DB.Column('private_id', DB.String(36), primary_key=True, nullable = False)
    public_id = DB.Column('public_id', DB.Integer, unique=True, nullable=False)
    email = DB.Column('email', DB.String(50), unique = True, nullable=False)
    first_name = DB.Column('first_name', DB.String(20), nullable=False)
    last_name = DB.Column('last_name', DB.String(20), nullable=False)
    university = DB.Column('school', DB.String(50), nullable=False)
    birthday = DB.Column('birthday', DB.String(10), nullable=False) # MM-DD-YYYY
    size = DB.Column('t-shirt_size', DB.String(5), nullable=False)
    short_answer = DB.Column("short_answer", DB.String(250), nullable=False)

    # optional fields
    optional_info = {}
    optional_info["gender"] = DB.Column('gender', DB.String(1)) #M or F or O (other or prefer not to say?)
    optional_info["ethnicity"] = DB.Column('ethnicity',DB.String(20))
    optional_info["major"] = DB.Column('major', DB.String(20))
    optional_info["dietary_rest"] = DB.Column("dietary_rest", DB.String(50))
    optional_info["num_hacks"] = DB.Column("num_hacks", DB.Integer)
    optional_info["linkedin"] = DB.Column("linkedin", DB.String(50))
    optional_info["github"] = DB.Column("github", DB.String(50))



    # Fill in the other attributes from DBSchema.md

    def __init__(self, email, firstName, lastName, university, birthday, size, short_answer, **kwargs):
        # Still need public ID and private ID, generate them from unique email
        guid = uuid4()
        self.private_id = str(guid)

        # guid.int is 128 bits.  Save some space since there won't be 2**128 applicants.
        self.public_id = guid.int % (2**16)

        # general info
        self.email = email
        self.first_name = firstName
        self.last_name = lastName
        self.university = university
        self.birthday = birthday
        self.size = size
        self. short_answer = short_answer

        for key, value in kwargs.items():
            self.optional_info[str(key)] = str(value)


    def __repr__(self):
        return "{ Attendee: email=%s, name=%s %s, school=%s }" % (self.email, self.first_name, self.last_name, self.school)
