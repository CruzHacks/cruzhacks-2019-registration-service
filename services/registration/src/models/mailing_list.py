"""Defines RDBMS table for mailing list."""
# pylint: disable=duplicate-code
from registration.src.db import DB

class MailingList(DB.Model):
    # pylint: disable=no-member, too-few-public-methods, too-many-instance-attributes
    """Table of a people's submitted registration info."""
    __tablename__ = 'mailing_list'

    email = DB.Column('email', DB.String(75), primary_key=True)

    def __init__(self, email):
        self.email = email

    def __repr__(self):
        return "{ Mailing List: email=%s }" % (self.email)
