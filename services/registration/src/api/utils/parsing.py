"""Parsing inputs or responses."""
from datetime import datetime

def is_valid_email(email):
    """Ensures an email has a very basic, possibly correct format.

    An email may have invalid characters or an invalid domain,
    but that will be found when the user does not confirm an email.

    :param email: email to validate
    :type  email: string
    """
    try:
        split = email.split('@')
        assert len(split) == 2
        domain = split[1]
        assert '.' in domain
    except AssertionError:
        return False
    return True

def datestring_to_datetime(datestring):
    """Converts a date (as a string) to a datetime object.

    :param datestring: date in the format of 'yyyy-mm-dd'
    :type  datestring: string
    :rtype: datetime
    """
    return datetime(*[int(s) for s in datestring.split('-')])

def strip_non_num(phone):
    """converts phone number to string with only digits"""
    return ''.join([i for i in phone if i.isdigit()])
