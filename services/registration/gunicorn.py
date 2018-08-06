from os import environ as env

if env.get('GUNICORN_AUTO_RELOAD', '').lower() == 'on':
    reload = True

bind = '0.0.0.0:8000'  # Open the server to listen on all NICs on port 8000.