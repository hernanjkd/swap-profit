
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
from notifications import send_email_message
def attach(app):

    @app.route('/create/token', methods=['POST'])
    def create_token():
        return jsonify( create_jwt(request.get_json()) ), 200

    @app.route('/test_email', methods=['GET'])
    def send_test_email():
        response = send_email_message('test','hernanjkd@gmail.com', {
            "message": "Holis papi"
        })
        return str(response), 200



    @app.route('/fill_database')
    def fill_database():

        lou = Users(
            email='lou@gmail.com',
            password=hash('loustadler')
        )
        db.session.add(lou)
        lou = Profiles(
            first_name='Luiz', 
            last_name='Stadler',
            nickname='Lou',
            hendon_url='https://pokerdb.thehendonmob.com/player.php?a=r&n=207424',
            profile_pic_url='https://pokerdb.thehendonmob.com/pictures/Lou_Stadler_Winner.JPG',
            user=lou
        )
        db.session.add(lou)

        cary = Users(
            email='katz234@gmail.com',
            password=hash('carykatz')
        )
        db.session.add(cary)
        cary = Profiles(
            first_name='Cary', 
            last_name='Katz',
            nickname='',
            hendon_url='https://pokerdb.thehendonmob.com/player.php?a=r&n=26721',
            profile_pic_url='https://pokerdb.thehendonmob.com/pictures/carykatzpic.png',
            user=cary
        )
        db.session.add(cary)

        kate = Users(
            email='hoang28974@gmail.com',
            password=hash('kateHoang')
        )
        db.session.add(kate)
        kate = Profiles(
            first_name='Kate', 
            last_name='Hoang',
            nickname='',
            hendon_url='https://pokerdb.thehendonmob.com/player.php?a=r&n=421758',
            profile_pic_url='https://pokerdb.thehendonmob.com/pictures/Hoang_2.jpg',
            user=kate
        )
        db.session.add(kate)

        nikita = Users(
            email='mikitapoker@gmail.com',
            password=hash('nikitapoker')
        )
        db.session.add(nikita)
        nikita = Profiles(
            first_name='Nikita', 
            last_name='Bodyakovskiy',
            nickname='Mikita',
            hendon_url='https://pokerdb.thehendonmob.com/player.php?a=r&n=159100',
            profile_pic_url='https://pokerdb.thehendonmob.com/pictures/NikitaBadz18FRh.jpg',
            user=nikita
        )
        db.session.add(nikita)

        heartland = Tournaments(
            name='Heartland Poker Tour - HPT Colorado, Black Hawk',
            address='261 Main St, Black Hawk, CO 80422',
            start_at=datetime(2019,10,11,12),
            end_at=datetime(2019,10,11,21)
        )
        db.session.add(heartland)

        stones = Tournaments(
            name='Stones Live Fall Poker Series',
            address='6510 Antelope Rd, Citrus Heights, CA 95621',
            start_at=datetime(2019,9,30,11),
            end_at=datetime(2019,10,1,22)
        )
        db.session.add(stones)

        wpt = Tournaments(
            name='WPT DeepStacks - WPTDS Sacramento',
            address='Thunder Valley Casino Resort, 1200 Athens Ave, Lincoln, CA 95648',
            start_at=datetime(2019,10,2,12),
            end_at=datetime(2019,10,2,22)
        )
        db.session.add(wpt)

        db.session.add(Flights(
            start_at = datetime(2019,10,11,12),
            end_at = datetime(2019,10,11,16),
            tournament = heartland,
            day = 1
        ))
        db.session.add(Flights(
            start_at = datetime(2019,10,11,16),
            end_at = datetime(2019,10,11,21),
            tournament = heartland,
            day = 1
        ))

        db.session.add(Flights(
            start_at = datetime(2019,9,30,12),
            end_at = datetime(2019,9,30,15),
            tournament = stones,
            day = 1
        ))
        db.session.add(Flights(
            start_at = datetime(2019,9,30,15),
            end_at = datetime(2019,9,30,21),
            tournament = stones,
            day = 1
        ))
        db.session.add(Flights(
            start_at = datetime(2019,10,1,12),
            end_at = datetime(2019,10,1,21),
            tournament = stones,
            day = 2
        ))

        db.session.add(Flights(
            start_at = datetime(2019,10,2,12),
            end_at = datetime(2019,10,2,22),
            tournament = wpt,
            day = 1
        ))

        db.session.add(Swaps(
            tournament=heartland,
            sender_user=lou,
            recipient_user=cary,
            percentage=10,
            winning_chips=None,
            due_at=(heartland.end_at + timedelta(days=4))
        ))

        db.session.add(Swaps(
            tournament=heartland,
            sender_user=cary,
            recipient_user=lou,
            percentage=10,
            winning_chips=None,
            due_at=(heartland.end_at + timedelta(days=4))
        ))

        db.session.add(Swaps(
            tournament=heartland,
            sender_user=nikita,
            recipient_user=kate,
            percentage=15,
            winning_chips=None,
            due_at=(heartland.end_at + timedelta(days=4))
        ))

        db.session.add(Swaps(
            tournament=heartland,
            sender_user=kate,
            recipient_user=nikita,
            percentage=15,
            winning_chips=None,
            due_at=(heartland.end_at + timedelta(days=4))
        ))

        db.session.add(Swaps(
            tournament=heartland,
            sender_user=lou,
            recipient_user=kate,
            percentage=5,
            winning_chips=None,
            due_at=(heartland.end_at + timedelta(days=4))
        ))

        db.session.add(Swaps(
            tournament=heartland,
            sender_user=kate,
            recipient_user=lou,
            percentage=5,
            winning_chips=None,
            due_at=(heartland.end_at + timedelta(days=4))
        ))

        db.session.add(Swaps(
            tournament=wpt,
            sender_user=lou,
            recipient_user=cary,
            percentage=10,
            winning_chips=10000,
            due_at=(wpt.end_at + timedelta(days=4))
        ))

        db.session.add(Swaps(
            tournament=wpt,
            sender_user=cary,
            recipient_user=lou,
            percentage=10,
            winning_chips=500,
            due_at=(wpt.end_at + timedelta(days=4))
        ))

        db.session.add(Swaps(
            tournament=wpt,
            sender_user=nikita,
            recipient_user=kate,
            percentage=15,
            winning_chips=100,
            due_at=(wpt.end_at + timedelta(days=4))
        ))

        db.session.add(Swaps(
            tournament=wpt,
            sender_user=kate,
            recipient_user=nikita,
            percentage=15,
            winning_chips=0,
            due_at=(wpt.end_at + timedelta(days=4))
        ))

        db.session.add(Swaps(
            tournament=wpt,
            sender_user=cary,
            recipient_user=kate,
            percentage=5,
            winning_chips=500,
            due_at=(wpt.end_at + timedelta(days=4))
        ))

        db.session.add(Swaps(
            tournament=wpt,
            sender_user=kate,
            recipient_user=cary,
            percentage=5,
            winning_chips=0,
            due_at=(wpt.end_at + timedelta(days=4))
        ))

        db.session.commit()

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



    return app