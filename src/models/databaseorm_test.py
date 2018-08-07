from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Attendee import Base, Attendee

engine = create_engine('sqlite:///testdb.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

attendee_test = Attendee(email = 'test@test.com', first_name = 'john', last_name = 'dude')
session.add(attendee_test)
session.commit()