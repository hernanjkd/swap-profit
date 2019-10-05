
import os
from flask import Flask, request, jsonify, url_for, redirect
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from flask_jwt_simple import JWTManager, jwt_required, create_jwt, decode_jwt, get_jwt
from utils import APIException, generate_sitemap, has_params
from dummy_data import buy_ins, flights, swaps, profiles, tournaments
from models import db, Users, Profiles, Tournaments, Swaps, Flights, Buy_ins, Transactions, Tokens
from datetime import datetime, timedelta
import hashlib

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

app.config['JWT_SECRET_KEY'] = '47fh38d3z2w8fhjks0wp9zm4nm8dsd9ss09ds21fn3l7a8xgds'
jwt = JWTManager(app)


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


###############################################################################
#
# Must always pass just one dictionary when using create_jwt(), even if empty
# The expiration is for timedelta, so any keyworded argument that fits it
#
#       create_jwt( {'id':100,'role':'admin','expires':{'days':4}} )
#
###############################################################################
@jwt.jwt_data_loader
def add_claims_to_access_token(kwargs):    
    now = datetime.utcnow()
    kwargs = kwargs if type(kwargs) is dict else {}
    id = kwargs['id'] if 'id' in kwargs else None
    role = kwargs['roles'] if 'roles' in kwargs else 'user'
    expires = kwargs['expires'] if 'expires' in kwargs else {'minutes': 15}
    
    return {
        'exp': now + timedelta(**expires),
        'iat': now,
        'nbf': now,
        'sub': id,
        'role': role
    }




#############################################################################
## DELETE ENDPOINT - JUST FOR TESTING - DELETE ENDPOINT - JUST FOR TESTING ##
#############################################################################
@app.route('/create/token', methods=['POST'])
def create_token():
    return jsonify( create_jwt(request.get_json()) )




@app.route('/user/validate/<token>', methods=['GET'])
def validate(token):
    
    jwt_data = decode_jwt(token)
    
    user = Users.query.filter_by(id=jwt_data['sub']).first()

    if not user.valid:
        user.valid = True
        db.session.commit()

    return redirect('https://www.google.com', code=300)




# id can me the user id, me, or all
@app.route('/user/<id>', methods=['GET'])
@jwt_required
def get_users(id):

    jwt_data = get_jwt()
    
    if id == 'me':
        user = Users.query.filter_by(id=jwt_data['sub']).first()
        return jsonify(user.serialize()), 200

    if id == 'all':
        if jwt_data['role'] == 'admin':
            return jsonify([x.serialize() for x in Users.query.all()]), 200
        else:
            return 'Invalid request', 401

    try:
        id = int(id)
    except:
        return 'Invalid id', 400
    else:
        user = Users.query.filter_by(id=id).first()
        if user:
            return jsonify(user.serialize()), 200
        else:
            return 'No user found', 404




@app.route('/user', methods=['POST'])
def register_user():

    body = request.get_json()

    missing_item = has_params(body, 'email', 'password')
    if missing_item:
        raise APIException("You need to specify the " + missing_item, status_code=400)

    m = hashlib.sha256()
    m.update(body['password'].encode('utf-8'))

    # If user exists and failed to validate his account
    user = Users.query.filter_by( email=body['email'], password=m.hexdigest() ).first()
    if user and not user.valid:
        return jsonify({
            'validation_link': 'http://127.0.0.1:3000/user/validate/' + create_jwt({'id': user.id})
        }), 200

    elif user and user.valid:
        return 'User already exists', 405
    
    db.session.add(Users(
        email=body['email'], 
        password=m.hexdigest()
    ))
    db.session.commit()
    
    user = Users.query.filter_by(email=body['email']).first()

    return jsonify({
        'msg': 'User was created successfully',
        'validation_link': 'http://127.0.0.1:3000/user/validate/' + create_jwt({'id': user.id})
    }), 200




@app.route('/user/token', methods=['POST'])
def login():

    body = request.get_json()

    missing_item = has_params(body, 'email', 'password')
    if missing_item:
        raise APIException('You need to specify the ' + missing_item, status_code=400)

    m = hashlib.sha256()
    m.update(body['password'].encode('utf-8'))

    user = Users.query.filter_by( email=body['email'], password=m.hexdigest() ).first()
    if user and user.valid:
        return jsonify({
            'jwt': create_jwt({
                'id': user.id,
                'expires': {'minutes': body['exp'] if 'exp' in body else 15}
            })
        }), 200

    return 'The log in information is incorrect', 401




@app.route('/tournaments', methods=['GET'])
def get_all_tournaments():
    return jsonify([x.serialize() for x in Tournaments.query.all()])




@app.route('/tournaments/<int:id>', methods=['GET'])
def get_tournament(id):
    return jsonify(Tournaments.query.filter_by(id=id).first().serialize())




@app.route('/profiles')
def get_all_profiles():
    return jsonify([x.serialize(long=True) for x in Profiles.query.all()])




@app.route('/profiles/<id>', methods=['GET'])
def get_profile(id):
    if id == 'me':
        return 'me'
    if not id.isnumeric():
        return 'id must be numeric'
    return 'is numeric'




@app.route('/swaps/all')
def get_all_swaps():
    return jsonify([x.serialize(long=True) for x in Swaps.query.all()])




if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT)
