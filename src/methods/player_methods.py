from utils import role_jwt_required
from sqlalchemy import desc
from flask import Flask, request, jsonify, url_for, redirect, render_template

def attach(app):

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

        buyin = Buy_ins.query.filter_by(
            user_id = id,
            flight_id = body['flight_id'],
            chips = body['chips'],
            table = body['table'],
            seat = body['seat']
        ).order_by(Buy_ins.id.desc()).first()

        return jsonify({ **buyin.serialize(), "name": name }), 200




    @app.route('/me/buy_ins/<int:id>', methods=['PUT'])
    @role_jwt_required(['user'])
    def update_buy_in(id):

        body = request.get_json()
        check_params(body)

        user_id = get_jwt()['sub']

        buyin = Buy_ins.query.get(id)

        if not buyin:
            raise APIException('Buy_in not found', 404)

        update_table(buyin, body, ignore=['user_id','flight_id','receipt_img_url'])

        db.session.commit()

        return jsonify(Buy_ins.query.get(id).serialize())

    return app