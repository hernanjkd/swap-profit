from flask import Flask, request, jsonify, url_for, redirect, render_template
from flask_jwt_simple import JWTManager, create_jwt, decode_jwt, get_jwt
from models import db, Users
from utils import APIException

def attach(app):

    @app.route('/create/token', methods=['POST'])
    def create_token():
        return jsonify( create_jwt(request.get_json()) ), 200

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