import requests
from flask import request, jsonify
from flask_jwt_simple import JWTManager, create_jwt, get_jwt, jwt_required
from sqlalchemy import desc
from utils import APIException, check_params, validation_link, update_table, sha256, role_jwt_required
from models import db, Users, Profiles, Tournaments, Swaps, Flights, Buy_ins, Transactions, Coins
from datetime import datetime
from populate_database import run_seeds

def attach(app):


    @app.route('/reset_database')
    @jwt_required
    def populate():

        if get_jwt()['role'] != 'admin':
            raise APIException('Access denied', 401)

        run_seeds()

        lou = Profiles.query.filter_by(nickname='Lou').first()

        return jsonify([
            {"Lou's id": lou.id},
            {"token_data": {
                "id": lou.id,
                "role": "admin",
                "exp": 600000
            }},
            {"token": create_jwt({
                        'id': lou.id,
                        'role': 'admin',
                        'exp': 600000
                    })}
        ])




    @app.route('/create/token', methods=['POST'])
    def create_token():
        return jsonify( create_jwt(request.get_json()) ), 200




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




    @app.route('/flights/<int:id>')
    def get_flights(id):
        if id == 'all':
            return jsonify([x.serialize() for x in Flights.query.all()])

        if id.isnumeric():
            flight = Flights.query.get(int(id))
            if flight is None:
                raise APIException('Flight not found', 404)
            return jsonify(flight.serialize())
        
        return jsonify({'message':'Invalid id'})




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




    @app.route('/flights/<int:id>', methods=['DELETE'])
    @role_jwt_required(['admin'])
    def delete_flight(id, **kwargs):
        db.session.delete( Flights.query.get(id) )
        db.session.commit()
        return jsonify({'message':'Flight deleted'}), 200




    @app.route('/tournaments/<int:id>', methods=['DELETE'])
    @role_jwt_required(['admin'])
    def delete_tournament(id, **kwargs):
        db.session.delete( Tournaments.query.get(id) )
        db.session.commit()
        return jsonify({'message':'Tournament deleted'}), 200




    @app.route('/buy_ins/<int:id>', methods=['DELETE'])
    @role_jwt_required(['admin'])
    def delete_buy_in(id, **kwargs):
        db.session.delete( Buy_ins.query.get(id) )
        db.session.commit()
        return jsonify({'message':'Buy in deleted'}), 200




    @app.route('/swaps', methods=['DELETE'])
    @role_jwt_required(['admin'])
    def delete_swap(**kwargs):
        body = request.get_json()
        db.session.delete( Swaps.query.get(body['sender_id'], body['recipient_id'], body['tournament_id']) )
        db.session.commit()
        return jsonify({'message':'Swap deleted'}), 200




    @app.route('/devices/<int:id>', methods=['DELETE'])
    @role_jwt_required(['admin'])
    def delete_device(id, **kwargs):
        body = request.get_json()
        db.session.delete()
        db.session.commit()
        return jsonify({'message':'Device deleted'})




    @app.route('/swaps/all', methods=['GET'])
    @role_jwt_required(['admin'])
    def get_swaps(**kwargs):

        return jsonify([x.serialize() for x in Swaps.query.all()])




    return app