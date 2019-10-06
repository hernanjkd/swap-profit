
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

app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
jwt = JWTManager(app)


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


###############################################################################
#
# Must always pass just one dictionary when using create_jwt(), even if empty
# The expiration is for timedelta, so any keyworded argument that fits it
#
#       create_jwt( {'id':100,'role':'admin','exp':15 )
#
###############################################################################
@jwt.jwt_data_loader
def add_claims_to_access_token(kwargs):    
    now = datetime.utcnow()
    kwargs = kwargs if type(kwargs) is dict else {}
    id = kwargs['id'] if 'id' in kwargs else None
    role = kwargs['role'] if 'role' in kwargs else 'user'
    exp = kwargs['exp'] if 'exp' in kwargs else 15
    
    return {
        'exp': now + timedelta(minutes=exp),
        'iat': now,
        'nbf': now,
        'sub': id,
        'role': role
    }




# Takes only one param 'user' because admin will have access to all endpoints
# def role_jwt_required(role='admin'):
#     def decorator(func):
        
#         @jwt_required
#         def wrapper(*args, **kwargs):         
#                 jwt_role = get_jwt()['role']            
#                 if (
#                     (role == 'admin' and jwt_role != 'admin') or
#                     (role == 'user' and (jwt_role != 'user' or jwt_role != 'admin'))
#                 )
#                     raise APIException('Access denied', status_code=401)

#             return func(*args, **kwargs)
        
#         return wrapper
#     return decorator





#############################################################################
## DELETE ENDPOINT - JUST FOR TESTING - DELETE ENDPOINT - JUST FOR TESTING ##
#############################################################################
@app.route('/create/token', methods=['POST'])
def create_token():
    return jsonify( create_jwt(request.get_json()) )




@app.route('/user/validate/<token>', methods=['GET'])
def validate(token):
    
    jwt_data = decode_jwt(token)
    
    if jwt_data['role'] == 'invalid':
        user = Users.query.filter_by(id=jwt_data['sub']).first()
        if not user.valid:
            user.valid = True
            db.session.commit()

    return jsonify({
        'msg': 'Your email has been validated',
        'jwt': create_jwt({
            'id': jwt_data['sub'],
            'role': 'user',
            'exp': 600000
        })
    })




@app.route('/user', methods=['POST'])
def register_user():

    body = request.get_json()
    validation_link = (
        os.environ.get('API_HOST') + '/user/validate/' + create_jwt({'id': user.id,'role':'invalid'})
    )

    missing_item = has_params(body, 'email', 'password')
    if missing_item:
        raise APIException("You need to specify the " + missing_item, status_code=400)

    m = hashlib.sha256()
    m.update(body['password'].encode('utf-8'))


    # If user exists and failed to validate his account
    user = Users.query.filter_by( email=body['email'], password=m.hexdigest() ).first()
    if user and not user.valid:
        return jsonify({'validation_link': validation_link}), 200

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
        'validation_link': validation_link
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
    if user:        
        if user.valid:
            return jsonify({
                'jwt': create_jwt({
                    'id': user.id,
                    'exp': body['exp'] if 'exp' in body else 15
                })
            }), 200
            
        return 'Email not validated', 405

    return 'The log in information is incorrect', 401




# id can me the user id, me, or all
@app.route('/profiles/<id>', methods=['GET'])
@jwt_required
def get_profiles(id):

    jwt_data = get_jwt()
    
    if id == 'me':
        user = Profiles.query.filter_by(id=jwt_data['sub']).first()
        return jsonify(user.serialize()), 200

    if id == 'all':
        if jwt_data['role'] == 'admin':
            return jsonify([x.serialize() for x in Profiles.query.all()]), 200
        else:
            return 'Invalid request', 401

    if not id.isnumeric():
        raise APIException('Invalid id', status_code=400)

    id = int(id)
    user = Profiles.query.filter_by(id=id).first()
    if user:
        return jsonify(user.serialize()), 200
    
    return 'No user found', 404




@app.route('/profiles', methods=['POST'])
@jwt_required
def register_profiles():
    
    body = request.get_json()

    missing_item = has_params(body, 'first_name', 'last_name')
    if missing_item:
        raise APIException('You need to specify the ' + missing_item, status_code=400)

    return 'Work in progress', 200




@app.route('/tournaments/<int:id>', methods=['GET'])
def get_tournament(id):
    return jsonify(Tournaments.query.filter_by(id=id).first().serialize())




@app.route('/swaps/all')
def get_all_swaps():
    return jsonify([x.serialize(long=True) for x in Swaps.query.all()])




if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT)
