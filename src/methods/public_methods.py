from flask import Flask, request, jsonify, url_for, redirect, render_template
from flask_jwt_simple import JWTManager, create_jwt, decode_jwt, get_jwt
from models import db, Users
from utils import APIException

def attach(app):

    @app.route('/users', methods=['POST'])
    def register_user():

        body = request.get_json()
        check_params(body, 'email', 'password')

        # If user exists and failed to validate his account
        user = Users.query.filter_by( email=body['email'], password=sha256(body['password']) ).first()
        if user and not user.valid:
            return jsonify({'validation_link': validation_link(user.id)}), 200

        elif user and user.valid:
            raise APIException('User already exists', 405)

        db.session.add(Users(
            email = body['email'],
            password = sha256(body['password'])
        ))
        db.session.commit()

        user = Users.query.filter_by(email=body['email']).first()

        return jsonify({
            'message': 'Please verify your email',
            'validation_link': validation_link(user.id)
        }), 200




    @app.route('/users/validate/<token>', methods=['GET'])
    def validate(token):

        jwt_data = decode_jwt(token)

        if jwt_data['role'] != 'validating':
            raise APIException('Incorrect token', 400)

        user = Users.query.filter_by(id = jwt_data['sub']).first()
        if not user:
            raise APIException('Invalid key payload', 400)

        if not user.valid:
            user.valid = True
            db.session.commit()

        return jsonify({
            'message': 'Your email has been validated',
            'jwt': create_jwt({
                'id': jwt_data['sub'],
                'role': 'user',
                'exp': 600000
            })
        }), 200




    return app