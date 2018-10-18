"""Defines RDBMS table for user model."""
from uuid import uuid4

class Volunteer(DB.model):
   # pylint: disable=no-member, too-few-public-methods, too-many-instance-attributes
   """Table of a volunteer's submitted info."""
   __tablename__ = 'volunteers'

   # required fields
   private_id = DB.Column('private_id', DB.String(36), primary_key=True, nullable=False)
   public_id = DB.Column('public_id', DB.Integer, unique=True, nullable=False)
   email = DB.Column('email', DB.String(50), unique=True, nullable=False)
   first_name = DB.Column('first_name', DB.String(20), nullable=False)
   last_name = DB.Column('last_name', DB.String(20), nullable=False)
   birthday = DB.Column('birthday', DB.String(10), nullable=False) # MM-DD-YYYY
   size = DB.Column('t-shirt_size', DB.String(5), nullable=False)
   short_answer = DB.Column("short_answer", DB.String(500), nullable=False)
   assoc_clubs = DB.Column("clubs", DB.String(150), nullable=False)
   availability = DB.Column(DB.String(100), nullable = False)

   # optional field
   dietary_rest = DB.Column("dietary_rest", DB.String(50), nullable=True)

   # pylint: disable=line-too-long, too-many-arguments
   def __init__(email, first_name, last_name, birthday, size, short_answer, assoc_clubs, availability, **kwargs):

      # Still need public ID and private ID, generate them from unique email
      guid = uuid4()
      self.private_id = str(guid)

      # guid.int is 128 bits.  Save some space since there won't be 2**128 applicants.
      self.public_id = guid.int % (2**16)

      self.email = email
      self.first_name = first_name
      self.last_name = last_name
      self.birthday = birthday
      self.size = size
      self.short_answer = short_answer
      self.assoc_clubs = assoc_clubs
      self.availability = availability

      if len(kwargs == 1):
         self.dietary_rest = kwargs['dietary_rest']


   def __repr__(self):
      return "{ Volunteer: email=%s, name=%s %s, school=%s }" % (
         self.email, self.first_name, self.last_name, self.school)
