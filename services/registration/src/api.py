"""Defines API endpoints."""
from flask_restful import Api, Resource
from registration.models.attendee import DB, Attendee, query_response_to_dict

API = Api()


@API.resource('/')
class Home(Resource):
    #pylint: disable=no-self-use,missing-docstring
    def get(self):
        return 'Hello, World.'


@API.resource('/register')
class Register(Resource):
    #pylint: disable=no-self-use,no-member
    """Test endpoint for getting/posting users from the DB."""
    def get(self):
        """Gets every row in Registrations table."""
        return [query_response_to_dict(r) for r in Registrations.query.all()]

    def post(self):
        """Creates a row in Registrations table."""
        DB.session.add(Attendee())
        DB.session.commit()
        return 'posted!'
