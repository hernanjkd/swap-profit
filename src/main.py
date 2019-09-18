
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from flask_jwt_simple import JWTManager, jwt_required, create_jwt, get_jwt_identity
from utils import APIException, generate_sitemap, verify_json
from models import db

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

buy_ins = [
    {
        "id": 1,
        "user_id": 1,
        "flight_id": 1,
        "receipt_img_url": "http://lorempixel.com/400/200/",
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07"
    },
    {
        "id": 2,
        "user_id": 1,
        "flight_id": 1,
        "receipt_img_url": "http://lorempixel.com/400/200/",
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07"
    },
    {
        "id": 3,
        "user_id": 2,
        "flight_id": 1,
        "receipt_img_url": "http://lorempixel.com/400/200/",
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07"
    },
    {
        "id": 4,
        "user_id": 2,
        "flight_id": 2,
        "receipt_img_url": "http://lorempixel.com/400/200/",
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07"
    },
    {
        "id": 5,
        "user_id": 3,
        "flight_id": 1,
        "receipt_img_url": "http://lorempixel.com/400/200/",
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07"
    },
    {
        "id": 6,
        "user_id": 3,
        "flight_id": 3,
        "receipt_img_url": "http://lorempixel.com/400/200/",
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07"
    },
    {
        "id": 7,
        "user_id": 3,
        "flight_id": 4,
        "receipt_img_url": "http://lorempixel.com/400/200/",
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07"
    },
    {
        "id": 8,
        "user_id": 3,
        "flight_id": 5,
        "receipt_img_url": "http://lorempixel.com/400/200/",
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07"
    }
]

flights = [
    {
        "id": 1,
        "start_at": "Wed, 11 Oct 2019 16:00:00 GMT",
        "end_at": "Wed, 11 Oct 2019 21:00:00 GMT",
        "tournament_id": 1,
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07",
        "buy_ins": list(filter(lambda x: x['flight_id'] == 1, buy_ins))
    },
    {
        "id": 2,
        "start_at": "Wed, 11 Oct 2019 16:00:00 GMT",
        "end_at": "Wed, 11 Oct 2019 21:00:00 GMT",
        "tournament_id": 1,
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07",
        "buy_ins": list(filter(lambda x: x['flight_id'] == 2, buy_ins))
    },
    {
        "id": 3,
        "start_at": "Mon, 30 Sep 2019 12:00:00 GMT",
        "end_at": "Mon, 30 Sep 2019 21:00:00 GMT",
        "tournament_id": 2,
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07",
        "buy_ins": list(filter(lambda x: x['flight_id'] == 3, buy_ins))
    },
    {
        "id": 4,
        "start_at": "Tue, 1 Oct 2019 12:00:00 GMT",
        "end_at": "Tue, 1 Oct 2019 21:00:00 GMT",
        "tournament_id": 2,
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07",
        "buy_ins": list(filter(lambda x: x['flight_id'] == 4, buy_ins))
    },
    {
        "id": 5,
        "start_at": "Wed, 11 Oct 2019 12:00:00 GMT",
        "end_at": "Wed, 11 Oct 2019 16:00:00 GMT",
        "tournament_id": 3,
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07",
        "buy_ins": list(filter(lambda x: x['flight_id'] == 5, buy_ins))
    },
]

swaps = [
    {
        "tournament_id": 1,
        "sender_id": 1,
        "recipient_id": 2,
        "percentage": 5,
        "winning_chips": None, # these will be null while they are playing
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07"
    },
    {
        "tournament_id": 1,
        "sender_id": 2,
        "recipient_id": 1,
        "percentage": 5,
        "winning_chips": None, # these will be null while they are playing
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07"
    },
    {
        "tournament_id": 1,
        "sender_id": 2,
        "recipient_id": 3,
        "percentage": 10,
        "winning_chips": None, # these will be null while they are playing
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07"
    },
    {
        "tournament_id": 1,
        "sender_id": 3,
        "recipient_id": 2,
        "percentage": 10,
        "winning_chips": None, # these will be null while they are playing
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07"
    },
    {
        "tournament_id": 2,
        "sender_id": 1,
        "recipient_id": 3,
        "percentage": 12,
        "winning_chips": None, # these will be null while they are playing
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07"
    },
    {
        "tournament_id": 2,
        "sender_id": 3,
        "recipient_id": 1,
        "percentage": 12,
        "winning_chips": None, # these will be null while they are playing
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07"
    },
    {
        "tournament_id": 2,
        "sender_id": 2,
        "recipient_id": 1,
        "percentage": 3,
        "winning_chips": 1000,
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07"
    },
    {
        "tournament_id": 2,
        "sender_id": 1,
        "recipient_id": 2,
        "percentage": 3,
        "winning_chips": 300,
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07"
    },
    {
        "tournament_id": 3,
        "sender_id": 2,
        "recipient_id": 3,
        "percentage": 20,
        "winning_chips": 500,
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07"
    },
    {
        "tournament_id": 3,
        "sender_id": 3,
        "recipient_id": 2,
        "percentage": 20,
        "winning_chips": 0,
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07"
    },
    {
        "tournament_id": 3,
        "sender_id": 1,
        "recipient_id": 3,
        "percentage": 16,
        "winning_chips": 500,
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07"
    },
    {
        "tournament_id": 3,
        "sender_id": 3,
        "recipient_id": 1,
        "percentage": 16,
        "winning_chips": 600,
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07"
    }
]

profiles = [
    {
        "id": 1,
        "first_name": "Cary",
        "last_name": "Katz",
        "username": "",
        "email": "katz234@gmail.com",
        "hendon_url": "https://pokerdb.thehendonmob.com/player.php?a=r&n=26721",
        "profile_picture_url": "https://pokerdb.thehendonmob.com/pictures/carykatzpic.png",
        "transactions": "list of transactions",
        "created_at": "Tue, 17 Sep 2019 04:23:59 GMT",
        "updated_at": "Tue, 17 Sep 2019 04:23:59 GMT",
        "tokens": 12,
        "swaps": list(filter(lambda x: x['sender_id'] == 1, swaps)),
        "buy_ins": list(filter(lambda x: x['user_id'] == 1, buy_ins))
    },
    {
        "id": 2,
        "first_name": "Kate",
        "last_name": "Hoang",
        "username": "",
        "email": "hoang234@gmail.com",
        "hendon_url": "https://pokerdb.thehendonmob.com/player.php?a=r&n=421758",
        "profile_picture_url": "https://pokerdb.thehendonmob.com/pictures/Hoang_2.jpg",
        "transactions": "list of transactions",
        "created_at": "Tue, 17 Sep 2019 04:23:59 GMT",
        "updated_at": "Tue, 17 Sep 2019 04:23:59 GMT",
        "tokens": 0,
        "swaps": list(filter(lambda x: x['sender_id'] == 2, swaps)),
        "buy_ins": list(filter(lambda x: x['flight_id'] == 2, buy_ins))
    },
    {
        "id": 3,
        "first_name": "Nikita",
        "last_name": "Bodyakovskiy",
        "username": "Mikita",
        "email": "bodyakov@gmail.com",
        "hendon_url": "https://pokerdb.thehendonmob.com/player.php?a=r&n=159100",
        "profile_picture_url": "https://pokerdb.thehendonmob.com/pictures/NikitaBadz18FRh.jpg",
        "transactions": "list of transactions",
        "created_at": "Tue, 17 Sep 2019 04:23:59 GMT",
        "updated_at": "Tue, 17 Sep 2019 04:23:59 GMT",
        "tokens": 5,
        "swaps": list(filter(lambda x: x['sender_id'] == 3, swaps)),
        "buy_ins": list(filter(lambda x: x['flight_id'] == 3, buy_ins))
    }
]

tournaments = [
    {
        "id": 1,
        "name": "Heartland Poker Tour - HPT Colorado, Black Hawk",
        "address": "261 Main St, Black Hawk, CO 80422",
        "start_at": "Wed, 11 Oct 2019 12:00:00 GMT",
        "end_at": "Wed, 11 Oct 2019 21:00:00 GMT",
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07",
        "swaps": "should we put a list of all the swaps for the tournament?",
        "flights": list(filter(lambda x: x['tournament_id'] == 1, flights))
    },
    {
        "id": 2,
        "name": "Stones Live Fall Poker Series",
        "address": "6510 Antelope Rd, Citrus Heights, CA 95621",
        "start_at": "Mon, 30 Sep 2019 11:00:00 GMT",
        "end_at": "Tue, 1 Oct 2019 22:00:00 GMT",
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07",
        "swaps": "should we put a list of all the swaps for the tournament?",
        "flights": list(filter(lambda x: x['tournament_id'] == 2, flights))
    },
    {
        "id": 3,
        "name": "WPT DeepStacks - WPTDS Sacramento",
        "address": "Thunder Valley Casino Resort, 1200 Athens Ave, Lincoln, CA 95648",
        "start_at": "Wed, 2 Oct 2019 12:00:00 GMT",
        "end_at": "Wed, 2 Oct 2019 21:00:00 GMT",
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07",
        "swaps": "should we put a list of all the swaps for the tournament?",
        "flights": list(filter(lambda x: x['tournament_id'] == 3, flights))
    }
]


@app.route('/tournament/<int:id>', methods=['GET'])
def get_tournament(id):
    return jsonify(list(filter(lambda x: x['id'] == id, tournaments))[0])

@app.route('/profile/<int:id>', methods=['GET'])
def get_profile(id):
    return jsonify(list(filter(lambda x: x['id'] == id, profiles))[0])

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT)

#############################################################################

# @app.route('/login', methods=['POST'])
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



# @app.route('/fill_database', methods=['GET'])
# def user():
    
    # user = Users(
    #     email = "ikelkwj32@gmail.com",
    #     password = hash("super secret password")
    # )
    # db.session.add(user)
    # db.session.add(Profiles(
    #     first_name = "Osvaldo",
    #     last_name = "Ratata",
    #     user = user
    # ))
    # db.session.commit()

    # tour = Tournaments(name="Grand Tour")
    # db.session.add(tour)
    # db.session.add(Flights(
    #     tournament = tour
    # ))
    # db.session.add(Flights(
    #     tournament = tour
    # ))
    # db.session.add(Flights(
    #     tournament = tour
    # ))
    # db.session.commit()

    # pics = list(map(lambda x: x.serialize(), Pictures.query.all()))
    # users = list(map(lambda x: x.serialize(), Users.query.all()))
    # prof = list(map(lambda x: x.serialize(), Profiles.query.all()))
    # tours = list(map(lambda x: x.serialize(), Tournaments.query.all()))
    # return jsonify(tours + prof)


#############################################################################

# @app.route('/register', methods=['POST'])
# def register_user():

#     # Register User
#     if request.method == 'POST':
#         body = request.get_json()

#         missing_item = verify_json(body, 'first_name', 'last_name', 'email', 'password')
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
