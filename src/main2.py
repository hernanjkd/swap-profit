
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from flask_jwt_simple import JWTManager, jwt_required, create_jwt, get_jwt_identity, get_jwt
from utils import APIException, generate_sitemap, has_params, expired
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

app.config['JWT_SECRET_KEY'] = '47fh38d3z2w8fhjks0wp9zm4ncmn36l7a8xgds'
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

#############################################################################


@app.route('/user/token')
def login():
    return (f'''
        <html>
        <body>
        <button onclick='send()'>FETCH</button>
        <div id='testing'></div>
        <script>
            function send() {{
                fetch('http://127.0.0.1:3000/user/test', {{
                        method: 'POST',
                        headers: {{ 
                            'Content-Type': 'application/json',
                            'authorization': "Bearer {create_jwt({'id':100,'roles':'admin','expires':{'seconds':5}})}"
                        }},
                        body: JSON.stringify({{'msg': 'received'}})
                    }})
                .then(resp => resp.json())
                .then(data => console.log(data))
            }}
        </script>
        </body>
        </html>
    ''')
    # return jsonify({
    #     'jwt': create_jwt(identity=5)
    # })

@app.route('/user/test', methods=['POST'])
@jwt_required
def test():
    if not request.is_json:
        return 'request is not json'
    params = request.get_json()
    jwt_data = get_jwt()
    
    return jsonify({'exp': expired(jwt_data['exp'])})
    # return jsonify(roles=jwt_data['roles'], sub=jwt_data['sub'], expires=jwt_data['exp'], body=params['msg'])

@app.route('/create/token')
def create_token():
    return create_jwt(identity=1)

# @app.route('/user/token', methods=['POST'])
# def login():
#     if request.method != 'POST':
#         return 'Invalid method', 404

#     body = request.get_json()

#     missing_item = has_params(body, 'email', 'password')
#     if missing_item:
#         raise APIException('You need to specify the ' + missing_item, status_code=400)

#     all_users = Users.query.all()
#     for user in all_users:
#         if user['email'] == body['email'] and user['password'] == hash(body['password']):
#             ret = {'jwt': create_jwt(identity=body['email'])}
#             return jsonify(ret), 200

#     return 'The log in information is incorrect', 401


# @app.route('/user', methods=['POST'])


# @app.route('/user/validate', methods=['GET'])


#############################################################################


@app.route('/fill_database')
def fill_database():
    
    lou = Profiles.query.filter_by(username='Lou').first()
    cary = Profiles.query.filter_by(first_name='Cary').first()
    kate = Profiles.query.filter_by(first_name='Kate').first()
    nikita = Profiles.query.filter_by(username='Mikita').first()

    tour = Tournaments.query.filter_by(id=5).first()
    
    # db.session.commit()

    return '<h2 style="text-align:center;padding-top:100px">DATA ADDED</h2>'

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
    # return jsonify(Profiles.query.filter_by(id=id).first().serialize(long=True))

@app.route('/swaps/all')
def get_all_swaps():
    return jsonify(list(map(lambda x: x.serialize(long=True), Swaps.query.all())))
    # return jsonify(list(map(lambda x: x.serialize(), Swaps.query.filter_by(sender_id=2))))



if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT)



#############################################################################

# @app.route('/register', methods=['POST'])
# def register_user():

#     # Register User
#     if request.method == 'POST':
#         body = request.get_json()

#         missing_item = has_params(body, 'first_name', 'last_name', 'email', 'password')
#         if missing_item:
#             raise APIException("You need to specify the " + missing_item, status_code=400)

#         obj = Users(first_name=body['first_name'], last_name=body['last_name'], 
#                     email=body['email'], password=hash(body['password'])

#         db.session.add(obj)
#         db.session.commit()
#         return "ok", 200

#     return "Invalid Method", 404


# @app.route('/user/<int:user_id>', methods=['PUT', 'GET', 'DELETE'])
# def handle_user(user_id):
#     """
#     Single user
#     """

#     # PUT request
#     if request.method == 'PUT':
#         body = request.get_json()
#         if body is None:
#             raise APIException("You need to specify the request body as a json object", status_code=400)

#         obj = user.query.get(user_id)
#         if obj is None:
#             raise APIException('User not found', status_code=404)

#         if "username" in body:
#             obj.username = body["username"]
#         if "email" in body:
#             obj.email = body["email"]
#         db.session.commit()

#         return jsonify(obj.serialize()), 200

#     # GET request
#     if request.method == 'GET':
#         obj = User.query.get(user_id)
#         if obj is None:
#             raise APIException('User not found', status_code=404)
#         return jsonify(obj.serialize()), 200

#     # DELETE request
#     if request.method == 'DELETE':
#         obj = user.query.get(user_id)
#         if obj is None:
#             raise APIException('User not found', status_code=404)
#         db.session.delete(obj)
#         db.session.commit()
#         return "ok", 200

#     return "Invalid Method", 404
