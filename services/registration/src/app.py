import os
from flask import Flask
from registration.src.db import db
from registration.src.api import api

app = Flask(__name__)

with app.app_context():
    db_uri = os.environ['SQLALCHEMY_DATABASE_URI']
    deployment_mode = os.getenv('DEPLOYMENT_MODE', 'prod').lower()

    # Set DB connection.  If not found, raises KeyError and exits.
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    # Assume we're not in dev.
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_RECORD_QUERIES'] = False
    app.config['SQLALCHEMY_ECHO'] = False

    db.init_app(app)
    api.init_app(app)

    # Set any dev deployment modes here.
    if deployment_mode == 'dev':
        app.logger.warning('You are in development mode.  Do not push code to master with this set!')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        app.config['SQLALCHEMY_RECORD_QUERIES'] = True
        app.config['SQLALCHEMY_ECHO'] = True
        db.drop_all()

    db.create_all() # Create any tables if they do not exist.

if __name__=='__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
