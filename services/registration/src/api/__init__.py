"""Defines API endpoints."""
from flask_restful import Api

from registration.src.api.accounts import User, Verify
from registration.src.api.announcement import SingleAnnouncement, AllAnnouncements
from registration.src.api.attendee import (
    AttendeeRegistration, AttendeeIsRegistered, AttendeeAddResume, AttendeeResumeExists
)
from registration.src.api.judge import JudgeRegistration, JudgeIsRegistered
from registration.src.api.mentor import MentorRegistration, MentorIsRegistered
from registration.src.api.volunteer import VolunteerRegistration, VolunteerIsRegistered
from registration.src.api.subscriber import SubscriberList

API = Api()

API.add_resource(User, '/accounts/users')
API.add_resource(Verify, '/accounts/users/verify')

API.add_resource(SingleAnnouncement, '/announcements')
API.add_resource(AllAnnouncements, '/announcements/all')

API.add_resource(AttendeeRegistration, '/register/attendee')
API.add_resource(AttendeeIsRegistered, '/register/attendee/is_registered')
API.add_resource(AttendeeAddResume, '/register/attendee/add_resume')
API.add_resource(AttendeeResumeExists, '/register/attendee/resume_exists')

API.add_resource(JudgeRegistration, '/register/judge')
API.add_resource(JudgeIsRegistered, '/register/judge/is_registered')

API.add_resource(MentorRegistration, '/register/mentor')
API.add_resource(MentorIsRegistered, '/register/mentor/is_registered')

API.add_resource(VolunteerRegistration, '/register/volunteer')
API.add_resource(VolunteerIsRegistered, '/register/volunteer/is_registered')

API.add_resource(SubscriberList, '/subscribe')
