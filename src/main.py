
import os
from flask import Flask, request, jsonify, url_for, redirect, render_template
from flask_migrate import Migrate
from admin import SetupAdmin
from flask_swagger import swagger
from flask_cors import CORS
from flask_jwt_simple import JWTManager, create_jwt, decode_jwt, get_jwt
from sqlalchemy import desc
from utils import APIException, generate_sitemap, check_params, validation_link, update_table, sha256, role_jwt_required
from models import db, Users, Profiles, Tournaments, Swaps, Flights, Buy_ins, Transactions, Tokens
from datetime import datetime, timedelta
from methods import player_methods, public_methods, sample_methods, admin_methods

def create_app(testing=False):
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    if testing:
        app.config['JWT_SECRET_KEY'] = 'dev_asdasd'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sample.sqlite'
        app.config['TESTING'] = True
    else:
        app.secret_key = os.environ.get('FLASK_KEY')
        app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    MIGRATE = Migrate(app, db)
    db.init_app(app)
    CORS(app)

    jwt = JWTManager(app)
    admin = SetupAdmin(app)

    @app.errorhandler(APIException)
    def handle_invalid_usage(error):
        return jsonify(error.to_dict()), error.status_code

    ###############################################################################
    #
    # Must always pass just one dictionary when using create_jwt(), even if empty
    # The expiration is for timedelta, so any keyworded argument that fits it
    #
    #       create_jwt( {'id':100,'role':'admin','exp':15} )
    #
    ###############################################################################
    @jwt.jwt_data_loader
    def add_claims_to_access_token(kwargs={}):
        now = datetime.utcnow()
        kwargs = kwargs if isinstance(kwargs, dict) else {}
        id = kwargs['id'] if 'id' in kwargs else None
        role = kwargs['role'] if 'role' in kwargs else 'invalid'
        exp = kwargs['exp'] if 'exp' in kwargs else 15

        return {
            'exp': now + timedelta(minutes=exp),
            'iat': now,
            'nbf': now,
            'sub': id,
            'role': role
        }

    app = sample_methods.attach(app)
    app = player_methods.attach(app)
    app = public_methods.attach(app)
    app = admin_methods.attach(app)

    return app

app = create_app()



if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT)
