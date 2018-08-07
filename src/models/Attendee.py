# Attendee.py
# Database ORM Model for Attendee
'''
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, Table

Base = declarative_base()

class Attendee(Base):
   __tablename__ = 'attendee'
   email = Column('email', String, primary_key = True, unique = True)
   first_name = Column('first_name', String)
   last_name = Column('last_name', String)
   school = Column('school', String)

   def __init__(self, email, fn, ln):
      self.email = email
      self.first_name = fn
      self.last_name = ln

   def __repr__(self):
      return( "Attendee: " + self.email + " , " + self.first_name + " " + self.last_name)


engine = create_engine('sqlite:///testdb.db')
Base.metadata.create_all(engine)'''


from flask_sqlalchemy import sqlalchemy


db = SQLalchemy()

class Attendee(db.Model):
   id_num = db.Column('id_num',db.Integer, primary_key = True)
   email = db.Column('email', db.String(50), unique = True)
   first_name = db.Column('first_name', db.String(50))
   last_name = db.Column('last_name', db.String(50))
   school = db.Column('school', db.String(50))

   def __init__(self, email, fn, ln, univ):
      self.email = email
      self.first_name = fn
      self.last_name = ln
      self.school = univ

   def __repr__(self):
      return "Attendee: email=%s, name=%s %s, school=%s" % (self.email, self.first_name, self.last_name, self.school)