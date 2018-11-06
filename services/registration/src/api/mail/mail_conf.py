import os
from flask import Flask, request, make_response, jsonify, render_template
from flask_mail import Mail, Message

app = Flask(__name__)
mail = Mail(app)

# REMOVE THIS LATER SET IN ENVIRONMENT VAR???
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD']
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route("/confirm", methods=["PUT"])
def sendconfirmation():
   try:
      name = request.form['name']
      email = request.form['email']

      msg = Message('Thanks for applying!', sender = os.environ['MAIL_USERNAME'], recipients = [email])
      msg.html = render_template('index.html', name = name)

      with app.open_resource("static/web-banner.png") as fp:
         msg.attach("banner.png", "image/png", fp.read())
         

      mail.send(msg)
      return make_response(jsonify(msg="Email sent!"), 200, {'Content-Type':'application/json'})
   except Exception as e:
      return make_response(jsonify(msg="error", error=str(e)), 404, {'Content-Type':'application/json'})






if __name__== "__main__":
   app.run(host=None, port=8080, debug=True)