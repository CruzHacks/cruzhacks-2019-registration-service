"""Defines RDBMS table for Announcement model."""
# pylint: disable=duplicate-code
from registration.src.db import DB

class Announcement(DB.Model):
    # pylint: disable=no-member, too-few-public-methods, too-many-instance-attributes
    """Table of a people's submitted registration info."""
    __tablename__ = 'announcements'

    title = DB.Column('title', DB.String(128), primary_key=True)
    post_date = DB.Column('post_date', DB.DateTime, primary_key=True)
    message = DB.Column('message', DB.String(256))

    # pylint: disable=too-many-arguments, too-many-locals
    def __init__(self, title, post_date, message=None):
        self.title = title
        self.post_date = post_date
        self.message = message

    def __repr__(self):
        return "{ Announcement: title=%s, post_date=%s, university=%s }" % (
            self.title, self.post_date, self.message)
