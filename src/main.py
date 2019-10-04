
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from flask_jwt_simple import JWTManager, jwt_required, create_jwt, get_jwt_identity, get_jwt
from utils import APIException, generate_sitemap, verify_json, expired
from dummy_data import buy_ins, flights, swaps, profiles, tournaments
from models import db, Users, Profiles, Tournaments, Swaps, Flights, Buy_ins, Transactions, Tokens
from datetime import datetime, timedelta

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
#       create_jwt( {'id':100,'roles':'admin','expires':{'days':4}} )
#
###############################################################################
@jwt.jwt_data_loader
def add_claims_to_access_token(kwargs):    
    now = datetime.utcnow()
    kwargs = kwargs if type(kwargs) is dict else {}
    id = kwargs['id'] if 'id' in kwargs.keys() else None
    roles = kwargs['roles'] if 'roles' in kwargs.keys() else 'user'
    expires = kwargs['expires'] if 'expires' in kwargs.keys() else {'minutes':5}
    
    return {
        'exp': now + timedelta(**expires),
        'iat': now,
        'nbf': now,
        'sub': id,
        'roles': roles
    }




# @app.route('/user/test', methods=['POST'])
# @jwt_required
# def test():
#     if not request.is_json:
#         return 'request is not json'
#     params = request.get_json()
#     jwt_data = get_jwt()
    
#     return jsonify({'exp': expired(jwt_data['exp'])})



# @app.route('/user/token', methods=['POST'])
# def login():
#     if request.method != 'POST':
#         return 'Invalid method', 404

#     body = request.get_json()

#     missing_item = verify_json(body, 'email', 'password')
#     if missing_item:
#         raise APIException('You need to specify the ' + missing_item, status_code=400)

#     all_users = Users.query.all()
#     for user in all_users:
#         if user['email'] == body['email'] and user['password'] == hash(body['password']):
#             ret = {'jwt': create_jwt(identity=body['email'])}
#             return jsonify(ret), 200

#     return 'The log in information is incorrect', 401



# @app.route('/user/validate', methods=['GET'])


#############################################################################



@app.route('/user', methods=['POST'])
def register_user():
    
    if request.method != 'POST':
        return "Invalid Method", 404

    body = request.get_json()

    missing_item = verify_json(body, 'email', 'password')
    if missing_item:
        raise APIException("You need to specify the " + missing_item, status_code=400)

    db.session.add(Users(
        email=body['email'], 
        password=hash(body['password'])
    ))
    db.session.commit()

    return jsonify([x.serialize() for x in Users.query.all()])
    #return "ok", 200



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
