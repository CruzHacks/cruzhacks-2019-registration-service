"""Defines API endpoints."""
#pylint: disable=unused-argument,invalid-name,no-member,no-self-use
import os

from flask_restful import Api, abort, Resource

from registration.src.api.attendee import AttendeeRegistration, AttendeeIsRegistered
from registration.src.api.judge import JudgeRegistration, JudgeIsRegistered
from registration.src.api.mentor import MentorRegistration, MentorIsRegistered
from registration.src.api.volunteer import VolunteerRegistration, VolunteerIsRegistered
from registration.src.api.mailing_list import SubscriberListConfirmation

API = Api()

API.add_resource(AttendeeRegistration, '/register/attendee')
API.add_resource(AttendeeIsRegistered, '/register/attendee/is_registered')

API.add_resource(JudgeRegistration, '/register/judge')
API.add_resource(JudgeIsRegistered, '/register/judge/is_registered')

API.add_resource(MentorRegistration, '/register/mentor')
API.add_resource(MentorIsRegistered, '/register/mentor/is_registered')

API.add_resource(VolunteerRegistration, '/register/volunteer')
API.add_resource(VolunteerIsRegistered, '/register/volunteer/is_registered')

API.add_resource(SubscriberListConfirmation, '/subscriber_confirmation')
