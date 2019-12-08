from flask import Flask, request, jsonify, url_for, redirect, render_template
from flask_jwt_simple import JWTManager, create_jwt, decode_jwt, get_jwt
from notifications import send_email

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

    return app