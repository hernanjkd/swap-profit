
from flask import request, jsonify, render_template
from flask_cors import CORS
from flask_jwt_simple import JWTManager, create_jwt, decode_jwt, get_jwt
from utils import APIException, check_params, validation_link, update_table, sha256, role_jwt_required
from models import db, Users, Profiles, Tournaments, Swaps, Flights, Buy_ins, Transactions, Tokens
from notifications import send_email

def attach(app):

    @app.route('/users', methods=['POST'])
    def register_user():

        body = request.get_json()
        check_params(body, 'email', 'password')

        # If user exists and failed to validate his account
        user = (Users.query
                .filter_by( email=body['email'], password=sha256(body['password']) )
                .first())

        if user and user.valid == False:
            
            data = {'validation_link': validation_link(user.id)}
            send_email( type='email_validation', to=user.email, data=data)
            
            return jsonify({'message':'Another email has been sent for email validation'})

        elif user and user.valid:
            raise APIException('User already exists', 405)

        db.session.add(Users(
            email = body['email'],
            password = sha256(body['password'])
        ))
        db.session.commit()

        user = Users.query.filter_by(email=body['email']).first()

        data = {'validation_link': validation_link(user.id)}
        send_email( type='email_validation', to=user.email, data=data)

        return jsonify({'message': 'Please verify your email'}), 200




    @app.route('/users/token', methods=['POST'])
    def login():

        body = request.get_json()
        check_params(body, 'email', 'password')

        user = Users.query.filter_by( email=body['email'], password=sha256(body['password']) ).first()

        if not user:
            raise APIException('The log in information is incorrect', 401)

        if not user.valid:
            raise APIException('Email not validated', 405)

        return jsonify({
            'jwt': create_jwt({
                'id': user.id,
                'role': 'user',
                'exp': body['exp'] if 'exp' in body else 15
            })
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