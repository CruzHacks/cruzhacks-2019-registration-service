from registration.src.db import DB


class User(DB.Model):
    # pylint: disable=no-member, too-few-public-methods, too-many-instance-attributes
    """Table of a people's submitted registration info."""
    __tablename__ = 'users'

    username = DB.Column('username', DB.String(64), primary_key=True)
    encrypted_password = DB.Column('encrypted_password', DB.Binary(60))

    # pylint: disable=too-many-arguments, too-many-locals
    def __init__(self, username, encrypted_password):
        self.username = username
        self.encrypted_password = encrypted_password

    def __repr__(self):
        return "{ User: username=%s, encrypted_password=%s }" % (
            self.username, self.encrypted_password)


class Dev(DB.Model):
    # pylint: disable=no-member, too-few-public-methods, too-many-instance-attributes
    """Table of a people's submitted registration info."""
    __tablename__ = 'devs'

    username = DB.Column('username', DB.String(64), DB.ForeignKey('users.username'), primary_key=True)

    # pylint: disable=too-many-arguments, too-many-locals
    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return "{ Dev: username=%s }" % (self.username)

class Director(DB.Model):
    # pylint: disable=no-member, too-few-public-methods, too-many-instance-attributes
    """Table of a people's submitted registration info."""
    __tablename__ = 'directors'

    username = DB.Column('username', DB.String(64), DB.ForeignKey('users.username'), primary_key=True)

    # pylint: disable=too-many-arguments, too-many-locals
    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return "{ Director: username=%s }" % (self.username)

class Organizer(DB.Model):
    # pylint: disable=no-member, too-few-public-methods, too-many-instance-attributes
    """Table of a people's submitted registration info."""
    __tablename__ = 'organizers'

    username = DB.Column('username', DB.String(64), DB.ForeignKey('users.username'), primary_key=True)

    # pylint: disable=too-many-arguments, too-many-locals
    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return "{ Organizer: username=%s }" % (self.username)
