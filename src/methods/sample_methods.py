from flask import Flask, request, jsonify, url_for, redirect, render_template
from flask_jwt_simple import JWTManager, create_jwt, decode_jwt, get_jwt

def attach(app):

    @app.route('/sendemail')
    def sendemailtest():
        msg = {'message':'Hello Hernan'}
        send_email(type='test',to='hernanjkd@gmail.com',data=msg)
        l = 'testing'
        return requests.get(f'http://127.0.0.1:3000/{l}').json()


    @app.route('/testing', methods=['GET'])
    def first_endpoint():
        return jsonify({ 'details': "All good my friend"}), 200

    return app