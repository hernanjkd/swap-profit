
import os
from flask import Flask, request, jsonify, url_for, redirect, render_template
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from flask_jwt_simple import JWTManager, jwt_required, create_jwt, decode_jwt, get_jwt
from utils import APIException, generate_sitemap, check_params, validation_link, update_table, sha256
from dummy_data import buy_ins, flights, swaps, profiles, tournaments
from models import db, Users, Profiles, Tournaments, Swaps, Flights, Buy_ins, Transactions, Tokens
from datetime import datetime, timedelta



def login():

    body = request.get_json()
    

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