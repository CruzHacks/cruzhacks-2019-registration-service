"""Defines API endpoints."""
#pylint: disable=unused-argument,invalid-name,no-member,no-self-use
import os

from flask_restful import Api, abort, Resource

from registration.src.api.attendee import AttendeeRegistration
from registration.src.api.judge import JudgeRegistration
from registration.src.api.mentor import MentorRegistration
from registration.src.api.volunteer import VolunteerRegistration

API = Api()
API.add_resource(AttendeeRegistration, '/register/attendee')
API.add_resource(JudgeRegistration, '/register/judge')
API.add_resource(MentorRegistration, '/register/mentor')
API.add_resource(VolunteerRegistration, '/register/volunteer')
