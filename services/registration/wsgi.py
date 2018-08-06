"""Connects WSGI to Flask app instance."""
from registration.src.app import APP as application

# Mapping APP -> application is required because wsgi looks
# specifically for the 'application' variable to run from.

if __name__ == '__main__':
    application.run()
