"""Defines API endpoints."""
#pylint: disable=unused-argument,invalid-name,no-member,no-self-use
import os

from flask_restful import Api

from registration.src.api.attendee import AttendeeRegistration
from registration.src.api.judge import JudgeRegistration

API = Api()
API.add_resource(AttendeeRegistration, '/register/attendee')
API.add_resource(JudgeRegistration, '/register/judge')
