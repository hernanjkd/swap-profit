
import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from admin import SetupAdmin
from flask_cors import CORS
from flask_jwt_simple import JWTManager
from utils import APIException
from datetime import datetime, timedelta
from methods import player_methods, public_methods, sample_methods, admin_methods
from models import db

def create_app(testing=False):
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    if testing:
        app.config['JWT_SECRET_KEY'] = 'dev_asdasd'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://sample.sqlite'
        app.config['TESTING'] = True
    else:
        app.secret_key = os.environ.get('FLASK_KEY')
        app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    MIGRATE = Migrate(app, db)
    db.init_app(app)
    CORS(app)

    jwt = JWTManager(app)
    SetupAdmin(app)

    @app.errorhandler(APIException)
    def handle_invalid_usage(error):
        return jsonify(error.to_dict()), error.status_code

    ######################################################################
    # Takes in a dictionary with id, role and expiration date in minutes
    #        create_jwt({ 'id': 100, 'role': 'admin', 'exp': 15 })
    ######################################################################
    @jwt.jwt_data_loader
    def add_claims_to_access_token(kwargs={}):
        now = datetime.utcnow()
        kwargs = kwargs if isinstance(kwargs, dict) else {}
        id = kwargs.get('id')
        role = kwargs.get('role', 'invalid')
        exp = kwargs.get('exp', 15)

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
