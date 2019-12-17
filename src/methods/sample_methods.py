from flask import Flask, jsonify
from notifications import send_email
import requests
import os

def attach(app):

    @app.route('/sendemail')
    def sendemailtest():
        msg = {'name':'Hello Hernan'}
        send_email(type='account_created',to='hernanjkd@gmail.com',data=msg)
        l = 'testing'
        return 'email sent'


    @app.route('/testing', methods=['GET'])
    def first_endpoint():
        return jsonify({ 'details': "All good my friend"}), 200

    @app.route('/mailgun')
    def get_logs():
        return jsonify( requests.get(
            f"https://api.mailgun.net/v3/{os.environ.get('MAILGUN_DOMAIN')}/events",
            auth=("api", os.environ.get("MAILGUN_API_KEY")),
            params={"begin"       : "Fri, 13 DEC 2019 09:00:00 -0000",
                    "ascending"   : "yes",
                    "limit"       :  25,
                    "pretty"      : "yes",
                    "recipient" : "hernanjkd@gmail.com"}).json())

    return app