import logging
from registration.src.api import app as application

# Mapping app -> application is required because wsgi looks
# specifically for the 'application' variable to run from.

if __name__=='__main__':
    application.run()