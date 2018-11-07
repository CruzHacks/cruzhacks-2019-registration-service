"""Sends confirmation email and adds users to email list"""
import os
from flask import Flask, request, make_response, jsonify
import requests

APP = Flask(__name__)

@APP.route("/confirm", methods=["POST"])
def sendconfirmation():
    """Sends confirmation in a post req"""
    url = 'https://us17.api.mailchimp.com/3.0/lists/c566e13387/members'
    email = request.form['email']
    request_made = requests.post(url, json={'email_address':email, 'status':'subscribed'},
                                 auth=('user', os.environ['MAIL_APIKEY']))

    if request_made.status_code == 404:
        return make_response(jsonify(msg="error"), 404, {'Content-Type':'application/json'})

    return make_response(jsonify(msg="email sent!"), 200, {'Content-Type':'application/json'})

if __name__ == "__main__":
    APP.run(host=None, port=8080, debug=True)
