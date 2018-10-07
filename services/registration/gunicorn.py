# pylint: skip-file
"""Config script for gunicorn."""
import os

if os.environ.get('GUNICORN_AUTO_RELOAD', '').lower() == 'on':
    reload = True

bind = '0.0.0.0:{}'.format(os.environ.get('PORT', 8000))  # Open the server to listen on all NICs.
