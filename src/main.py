
import os
from flask import Flask, request, jsonify, url_for, redirect, render_template
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from flask_jwt_simple import JWTManager, jwt_required, create_jwt, decode_jwt, get_jwt
from sqlalchemy import desc
from utils import APIException, generate_sitemap, check_params, validation_link, update_table, sha256
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
#       create_jwt( {'id':100,'role':'admin','exp':15} )
#
###############################################################################
@jwt.jwt_data_loader
def add_claims_to_access_token(kwargs):    
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




# Notes: 'admin' will have access even if arg not passed
def role_jwt_required(valid_roles=['invalid']):
    def decorator(func):
        
        @jwt_required
        def wrapper(*args, **kwargs):         
            
            jwt_role = get_jwt()['role']
            valid = True if jwt_role == 'admin' else False

            for role in valid_roles:
                if role == jwt_role:
                    valid = True
                    
            if not valid:    
                raise APIException('Access denied', 401)

            return func(*args, **kwargs)
        
        # change wrapper name so it can be used for more than one function
        wrapper.__name__ = func.__name__

        return wrapper
    return decorator




#############################################################################
## DELETE ENDPOINT - JUST FOR TESTING - DELETE ENDPOINT - JUST FOR TESTING ##
#############################################################################
@app.route('/create/token', methods=['POST'])
def create_token():
    return jsonify( create_jwt(request.get_json()) ), 200

@app.route('/testing')
# @role_jwt_required(['user'])
def testing():
    
    raise APIException('read this msg', 406)

@app.route('/fill_database')
def fill_database():
    return jsonify({'message':'ok'}), 200

@app.route('/tournaments', methods=['POST'])
def add_tournament():
    body = request.get_json()
    db.session.add(Tournaments(
        name = body['name'],
        address = body['address'],
        start_at = datetime( *body['start_at'] ),
        end_at = datetime( *body['end_at'] ),
        longitude = None,
        latitude = None
    ))
    db.session.commit()
    search = {
        'name': body['name'],
        'start_at': datetime( *body['start_at'] )
    }
    return jsonify(Tournaments.query.filter_by(**search).first().serialize()), 200

@app.route('/flights/<id>')
def get_flights(id):
    if id == 'all':
        return jsonify([x.serialize() for x in Flights.query.all()])

@app.route('/flights', methods=['POST'])
def create_flight():
    body = request.get_json()
    db.session.add(Flights(
        tournament_id = body['tournament_id'],
        start_at = datetime( *body['start_at'] ),
        end_at = datetime( *body['end_at'] ),
        day = body['day']
    ))
    db.session.commit()
    search = {
        'tournament_id': body['tournament_id'],
        'start_at': datetime(*body['start_at']),
        'end_at': datetime(*body['end_at']),
        'day': body['day']
    }
    return jsonify(Flights.query.filter_by(**search).first().serialize()), 200

@app.route('/buy_ins/<id>')
def get_buyins(id):
    if id == 'all':
        return jsonify([x.serialize() for x in Buy_ins.query.all()])
    return jsonify(Buy_ins.query.get(int(id)).serialize())

@app.route('/flights/<id>', methods=['DELETE'])
def delete_flight(id):
    db.session.delete( Flights.query.get(id) )
    db.session.commit()
    return jsonify({'message':'hoe hoe hoe'}), 200

@app.route('/tournaments/<id>', methods=['DELETE'])
def delete_tournament(id):
    db.session.delete( Tournaments.query.get(id) )
    db.session.commit()
    return jsonify({'message':'Tournament deleted by jolly o Saint Nick'}), 200

@app.route('/buy_ins/<id>', methods=['DELETE'])
def delete_buy_in(id):
    db.session.delete( Buy_ins.query.get(id) )
    db.session.commit()
    return jsonify({'message':'Buy in deleted, and Santa will put you in the naughty list if you contine deleting stuff'}), 200

@app.route('/swaps', methods=['DELETE'])
def delete_swap():
    body = request.get_json()
    db.session.delete( Swaps.query.get(body['sender_id'], body['recipient_id'], body['tournament_id']) )
    db.session.commit()
    return jsonify({'message':"Swap deleted from Santa's list"}), 200
#############################################################################
## DELETE ENDPOINT - JUST FOR TESTING - DELETE ENDPOINT - JUST FOR TESTING ##
#############################################################################




@app.route('/users/validate/<token>', methods=['GET'])
def validate(token):
    
    jwt_data = decode_jwt(token)
    
    if jwt_data['role'] != 'validating':
        raise APIException('Incorrect token', 400)

    user = Users.query.get(jwt_data['sub'])
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




@app.route('/users', methods=['POST'])
def register_user():

    body = request.get_json()
    check_params(body, 'email', 'password')

    # If user exists and failed to validate his account
    user = Users.query.filter_by( email=body['email'], password=sha256(body['password']) ).first()
    if user and not user.valid:
        return jsonify({'validation_link': validation_link(user.id)}), 200

    elif user and user.valid:
        raise APIException('User already exists', 405)
    
    db.session.add(Users(
        email = body['email'], 
        password = sha256(body['password'])
    ))
    db.session.commit()
    
    user = Users.query.filter_by(email=body['email']).first()

    return jsonify({
        'message': 'Please verify your email',
        'validation_link': validation_link(user.id)
    }), 200




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




@app.route('/users/<id>/email', methods=['PUT'])
@role_jwt_required(['user'])
def update_email(id):

    if id == 'me':
        id = str(get_jwt()['sub'])

    if not id.isnumeric():
        raise APIException('Invalid id: ' + id, 400)

    body = request.get_json()
    check_params(body, 'email', 'password', 'new_email')

    user = Users.query.filter_by( id=int(id), email=body['email'], password=sha256(body['password']) ).first()
    if not user:
        raise APIException('Invalid parameters', 400)

    user.valid = False
    user.email = body['new_email']

    db.session.commit()

    return jsonify({
        'message': 'Please verify your new email',
        'validation_link': validation_link(user.id)
    }), 200




@app.route('/users/reset_password/<token>', methods=['GET','PUT'])
def html_reset_password(token):

    jwt_data = decode_jwt(token)    
    if jwt_data['role'] != 'password':
        raise APIException('Access denied', 401)

    if request.method == 'GET':
        return render_template('reset_password.html', data={
            'host': os.environ.get('API_HOST'),
            'token': token
        })

    # request.method == 'PUT'
    body = request.get_json()
    check_params(body, 'email', 'password')

    user = Users.query.filter_by(id = jwt_data['sub'], email = body['email']).first()
    if not user:
        raise APIException('User not found', 404)

    user.password = sha256(body['password'])

    db.session.commit()

    return jsonify({'message': 'Your password has been updated'}), 200

    
    




@app.route('/users/<id>/password', methods=['PUT'])
@role_jwt_required(['user'])
def reset_password(id):

    if id == 'me':
        id = str(get_jwt())['sub']

    if not id.isnumeric():
        raise APIException('Invalid id: ' + id, 400)
    
    
    if request.args.get('forgot') == 'true':        
        return jsonify({
            'message': 'A link has been sent to your email to reset the password',
            'link': os.environ.get('API_HOST') + '/users/reset_password/' + create_jwt({'id':id, 'role':'password'})
        }), 200


    body = request.get_json()
    check_params(body, 'email', 'password', 'new_password')

    user = Users.query.filter_by( id=int(id), email=body['email'], password=sha256(body['password']) ).first()
    if not user:
        raise APIException('Invalid parameters', 400)

    user.password = sha256(body['new_password'])

    db.session.commit()

    return jsonify({'message': 'Your password has been changed'}), 200




@app.route('/users/forgot_password/<token>', methods=['POST','PUT'])
def forgot_password(token):
    
    jwt_data = decode_jwt(token)

    return 'ok'




# id can be the user id, 'me' or 'all'
@app.route('/profiles/<id>', methods=['GET'])
@role_jwt_required(['user'])
def get_profiles(id):

    jwt_data = get_jwt()

    if id == 'all':
        if jwt_data['role'] != 'admin':
            raise APIException('Access denied', 401)
        
        return jsonify([x.serialize(long=True) for x in Profiles.query.all()]), 200

    if id == 'me':
        id = str(jwt_data['sub'])

    if not id.isnumeric():
        raise APIException('Invalid id: ' + id, 400)

    user = Profiles.query.get(int(id))
    if not user:
        raise APIException('User not found', 404)
    
    return jsonify(user.serialize(long=True)), 200




@app.route('/profiles', methods=['POST'])
@role_jwt_required(['user'])
def register_profile():
    
    user = Users.query.get(get_jwt()['sub'])
    if not user:
        raise APIException('User not found', 404)

    body = request.get_json()
    check_params(body, 'first_name', 'last_name')

    db.session.add(Profiles(
        first_name = body['first_name'],
        last_name = body['last_name'],
        nickname = body['nickname'] if 'nickname' in body else None,
        hendon_url = body['hendon_url'] if 'hendon_url' in body else None,
        user = user
    ))
    db.session.commit()

    return jsonify({'message':'ok'}), 200




@app.route('/profiles/<id>', methods=['PUT'])
@role_jwt_required(['user'])
def update_profile(id):

    if id == 'me':
        id = str(get_jwt())['sub']

    if not id.isnumeric():
        raise APIException('Invalid id: ' + id, 400)

    prof = Profiles.query.get(int(id))
    if not prof:
        raise APIException('User not found', 404)

    body = request.get_json()    
    check_params(body)
    
    update_table(prof, body, ignore=['profile_pic_url'], action=actions.update_user)

    db.session.commit()

    return jsonify(prof.serialize())




@app.route('/profiles/me/image', methods=['PUT'])
@role_jwt_required(['user'])
def upload_prof_pic():

    id = get_jwt()['sub']

    return 'ok'




# Can search by id, 'name' or 'all'
@app.route('/tournaments/<id>', methods=['GET'])
@role_jwt_required(['user'])
def get_tournaments(id):

    if id == 'all':
        return jsonify([x.serialize() for x in Tournaments.query.all()]), 200

    if id.isnumeric():
        trnmt = Tournaments.query.get(int(id))
    else:
        trnmt = Tournaments.query.filter(Tournaments.name.ilike(f'%{id}%')).all()
    
    if not trnmt:
        raise APIException('Tournament not found', 404)
    
    if isinstance(trnmt, list):
        return jsonify([x.serialize() for x in trnmt]), 200

    return jsonify(trnmt.serialize()), 200




@app.route('/swaps/<id>', methods=['GET'])
def get_swaps(id):

    if id == 'all':
        return jsonify([x.serialize() for x in Swaps.query.all()])

    prof = Profiles.query.get(7)
    return str(prof.available_percentage(1))
    # return jsonify( [x.serialize() for x in Swaps.query.all()] )




@app.route('/me/swaps', methods=['POST'])
@role_jwt_required(['user'])
def create_swap():
    
    id = int(get_jwt()['sub'])

    # get sender user
    sender = Profiles.query.get(id)
    if not sender:
        raise APIException('User not found', 404)
    
    body = request.get_json()
    check_params(body, 'tournament_id', 'recipient_id', 'percentage')

    # get recipient user
    recipient = Profiles.query.get(body['recipient_id'])
    if not recipient:
        raise APIException('Recipient user not found', 404)

    if Swaps.query.get((id, body['recipient_id'], body['tournament_id'])):
        raise APIException('Swap already exists, can not duplicate', 400)

    sender_availability = sender.available_percentage( body['tournament_id'] )
    if body['percentage'] > sender_availability:
        raise APIException(('Swap percentage too large. You can not exceed 50% per tournament. '
                            f'You have available: {sender_availability}%'), 400)

    recipient_availability = recipient.available_percentage( body['tournament_id'] )
    if body['percentage'] > recipient_availability:
        raise APIException(('Swap percentage too large for recipient. '
                            f'He has available to swap: {recipient_availability}%'), 400)

    db.session.add(Swaps(
        sender_id = id,
        tournament_id = body['tournament_id'],
        recipient_id = body['recipient_id'],
        percentage = body['percentage']
    ))
    db.session.add(Swaps(
        sender_id = body['recipient_id'],
        tournament_id = body['tournament_id'],
        recipient_id = id,
        percentage = body['percentage']
    ))
    db.session.commit()

    return jsonify({'message':'ok'}), 200




# JSON receives a counter_percentage to update the swap of the recipient
@app.route('/me/swaps', methods=['PUT'])
@role_jwt_required(['user'])
def update_swap():

    id = int(get_jwt()['sub'])

    # get sender user
    sender = Profiles.query.get(id)
    if not sender:
        raise APIException('User not found', 404)
    
    body = request.get_json()
    check_params(body, 'tournament_id', 'recipient_id')

    # get recipient user
    recipient = Profiles.query.get(body['recipient_id'])
    if not recipient:
        raise APIException('Recipient user not found', 404)

    # get swap
    swap = Swaps.query.get((id, recipient.id, body['tournament_id']))
    counter_swap = Swaps.query.get((recipient.id, id, body['tournament_id']))
    if not swap or not counter_swap:
        raise APIException('Swap not found', 404)

    if 'percentage' in body:

        percentage = abs(body['percentage'])
        counter = abs(body['counter_percentage']) if 'counter_percentage' in body else percentage

        sender_availability = sender.available_percentage( body['tournament_id'] )
        if percentage > sender_availability:
            raise APIException(('Swap percentage too large. You can not exceed 50% per tournament. '
                                f'You have available: {sender_availability}%'), 400)

        recipient_availability = recipient.available_percentage( body['tournament_id'] )
        if counter > recipient_availability:
            raise APIException(('Swap percentage too large for recipient. '
                                f'He has available to swap: {recipient_availability}%'), 400)

        # So it can be updated correctly with the update_table funcion
        body['percentage'] = swap.percentage + percentage
        update_table(counter_swap, {'percentage': counter_swap.percentage + counter})

    update_table(swap, body, ignore=['tournament_id','recipient_id','paid','counter_percentage'])

    db.session.commit()

    return jsonify(swap.serialize())




@app.route('/swaps/me/tournament/<int:id>', methods=['GET'])
@role_jwt_required(['user'])
def get_swaps_actions(id):

    user_id = int(get_jwt()['sub'])

    prof = Profiles.query.get(user_id)
    if not prof:
        raise APIException('User not found', 404)

    return jsonify(prof.get_swaps_actions(id))






@app.route('/users/me/swaps/<id>/done', methods=['PUT'])
@role_jwt_required(['user'])
def set_swap_paid(id):

    id = int(get_jwt()['sub'])

    # get sender user
    sender = Profiles.query.get(id)
    if not sender:
        raise APIException('User not found', 404)
    
    body = request.get_json()
    check_params(body, 'tournament_id', 'recipient_id')

    swap = Swaps.query.get(id, body['recipient_id'], body['tournament_id'])

    swap.paid = True

    db.session.commit()

    return jsonify({'message':'Swap has been paid'})




@app.route('/me/buy_ins', methods=['GET'])
@role_jwt_required(['user'])
def get_buy_in():
    
    id = int(get_jwt()['sub'])

    return jsonify({'message':'ok'}), 200




@app.route('/me/buy_ins', methods=['POST'])
@role_jwt_required(['user'])
def create_buy_in():

    body = request.get_json()
    check_params(body, 'flight_id', 'chips', 'table', 'seat')

    id = int(get_jwt()['sub'])

    prof = Profiles.query.get(id)
    if not prof:
        raise APIException('User not found', 404)

    buyin = Buy_ins(
        user_id = id,
        flight_id = body['flight_id'],
        chips = body['chips'],
        table = body['table'],
        seat = body['seat']
    )
    db.session.add(buyin)
    db.session.commit()

    name = prof.nickname if prof.nickname else f'{prof.first_name} {prof.last_name}'
    
    # Get the latest entry by checking the created_at
    buyin = Buy_ins.query.filter_by(
        user_id = id,
        flight_id = body['flight_id'],
        chips = body['chips'],
        table = body['table'],
        seat = body['seat']
    ).first()

    return jsonify({ **buyin.serialize(), "name": name }), 200
    



@app.route('/me/buy_ins/<int:id>', methods=['PUT'])
@role_jwt_required(['user'])
def update_buy_in(id):

    body = request.get_json()
    check_params(body)

    user_id = int(get_jwt()['sub'])

    buyin = Buy_ins.query.get(id)

    update_table(buyin, body, ignore=['user_id','flight_id','receipt_img_url'])

    db.session.commit()

    return jsonify(Buy_ins.query.get(id).serialize())




@app.route('/me/swap_tracker', methods=['GET'])
@role_jwt_required(['user'])
def swap_tracker():

    id = int(get_jwt()['sub'])

    buyin = Buy_ins.query.filter_by(user_id=id).order_by(Buy_ins.id.desc()).first()
    if not buyin:
        raise APIException('Buy_in not found', 404)

    swaps = Swaps.query.filter_by(
        sender_id = id,
        tournament_id = buyin.flight.tournament_id
    )
    if not swaps:
        return jsonify({'message':'You have no live swaps in this tournament'})

    now = datetime.utcnow()
    trnmt = (Tournaments.query.filter(Tournaments.start_at < now)
                             .filter(Tournaments.end_at > now)).first()
    if not trnmt:
        raise APIException('No current tournaments')


    return jsonify({
        'tournament': trnmt
        'my_current_buy_in': buyin.serialize(),
        'others_swaps': [x.serialize() for x in swaps]
    })




if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT)
