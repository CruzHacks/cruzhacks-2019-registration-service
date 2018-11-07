import os
import requests
from flask import Flask, request, make_response, jsonify

app = Flask(__name__)

@app.route("/confirm", methods=["POST"])
def sendconfirmation():
   url = 'https://us17.api.mailchimp.com/3.0/lists/c566e13387/members'
   email = request.form['email']
   r = requests.post(url, json={'email_address':email, 'status':'subscribed'}, auth=('user', os.environ['MAIL_APIKEY']))

   if r.status_code == 200:
      return make_response(jsonify(msg="email sent!"), 200, {'Content-Type':'application/json'})

   else:
      return make_response(jsonify(msg="error"), 404, {'Content-Type':'application/json'})

if __name__== "__main__":
   app.run(host=None, port=8080, debug=True)