"""Defines API endpoints."""
#pylint: disable=unused-argument,invalid-name,no-member,no-self-use
import os

from flask_restful import Api

from registration.src.api import attendees

API = Api()
API.add_resource(attendees.Register, '/register/attendee')
