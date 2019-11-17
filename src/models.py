from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import datetime

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    valid = db.Column(db.Boolean, default=False)

    profile = db.relationship('Profiles', back_populates='user', uselist=False)
    transactions = db.relationship('Transactions', back_populates='user')
    tokens = db.relationship('Tokens', back_populates='user')

    def __repr__(self):
        return f'<Users {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "valid": self.valid,
            "created_at": "",
            "updated_at": ""
        }



class Profiles(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    nickname = db.Column(db.String(100))
    hendon_url = db.Column(db.String(200))
    profile_pic_url = db.Column(db.String(250), default=None)
    roi = db.Column(db.Float)

    user = db.relationship('Users', back_populates='profile', uselist=False)
    buy_ins = db.relationship('Buy_ins', back_populates='user')
    # sending_swaps
    # receiving_swaps

    def __repr__(self):
        return f'<Profiles {self.first_name} {self.last_name}>'

    def available_percentage(self, tournament_id):
        total = 0
        for swap in self.sending_swaps:
            if swap.tournament_id == tournament_id:
                if swap.status != 'rejected' and swap.status != 'unable to contact': 
                    total += swap.percentage
        return 50 - total

    def get_swaps_actions(self, tournament_id):
        actions = 0
        swaps = 0
        for swap in self.sending_swaps:
            if swap.tournament_id == tournament_id:
                if swap.status != 'rejected' and swap.status != 'unable to contact':
                    actions += swap.percentage
                    swaps += 1
        return {
            'actions': actions,
            'swaps': swaps
        }

    def testing(self):
        return jsonify({'msg':'working'})

    def serialize(self, long=False):
        json = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "nickname": self.nickname,
            "email": self.user.email,
            "profile_pic_url": self.profile_pic_url,
            "hendon_url": self.hendon_url,
            "roi": self.roi
        }
        if long:
            return {
                **json,
                "valid": self.user.valid,
                "created_at": "",
                "updated_at": "",
                "receiving_swaps": [x.serialize() for x in self.receiving_swaps],
                "buy_ins": [x.serialize() for x in self.buy_ins] 
            }
        return json



class Swaps(db.Model):
    __tablename__ = 'swaps'
    sender_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), primary_key=True)
    recipient_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.id'), primary_key=True)
    percentage = db.Column(db.Integer, nullable=False)
    winning_chips = db.Column(db.Integer, default=None)
    due_at = db.Column(db.DateTime, default=None)
    paid = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='pending')

    tournament = db.relationship('Tournaments', back_populates='swaps')
    sender_user = db.relationship('Profiles', foreign_keys=[sender_id], backref='sending_swaps')
    recipient_user = db.relationship('Profiles', foreign_keys=[recipient_id], backref='receiving_swaps')

    def __repr__(self):
        return f'<Swaps email:{self.user.email} recipient_user:{self.recipient_id} tournament:{self.tournament.name}>'

    def serialize(self, long=False, sender=False, percentage=False):
        # Being used in Profiles method
        if percentage:
            return {"percentage": self.percentage}
        if sender:
            return {
                "recipient_id": self.recipient_id,
                "tournament_id": self.tournament_id,
                "due_at": self.due_at,
                "winning_chips": self.winning_chips,
                "status": self.status,
                "paid": self.paid
            }
        json = {
            "tournament_id": self.tournament_id,
            "percentage": self.percentage,
            "winning_chips": self.winning_chips,
            "due_at": self.due_at,
            "status": self.status,
            "sender_user": self.sender_user.serialize(),
            "recipient_user": self.recipient_user.serialize()
        }
        if long:
            return {
                **json,
                "paid": self.paid,
                "created_at": "",
                "updated_at": ""
            }
        return json



class Tournaments(db.Model):
    __tablename__ = 'tournaments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    address = db.Column(db.String(250))
    start_at = db.Column(db.DateTime)
    end_at = db.Column(db.DateTime)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)

    flights = db.relationship('Flights', back_populates='tournament')
    swaps = db.relationship('Swaps', back_populates='tournament')

    def __repr__(self):
        return f'<Tournament {self.name}>'

    @staticmethod
    def get_live(user_id):
        now = datetime.utcnow()
        return (Tournaments.query
                    .filter( Tournaments.start_at > now )
                    .filter( Tournaments.end_at < now )
                    .filter( Tournaments.flights.any( Flights.buy_ins.any( user_id = user_id )) ))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "start_at": self.start_at,
            "end_at": self.end_at,
            "longitude": self.longitude,
            "latitude": self.latitude,
            "created_at": "",
            "updated_at": "",
            "flights": [x.serialize() for x in self.flights]
        }



class Flights(db.Model):
    __tablename__ = 'flights'
    id = db.Column(db.Integer, primary_key=True)
    start_at = db.Column(db.DateTime)
    end_at = db.Column(db.DateTime)
    day = db.Column(db.Integer)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.id'))

    tournament = db.relationship('Tournaments', back_populates='flights')
    buy_ins = db.relationship('Buy_ins', back_populates='flight')

    def __repr__(self):
        return f'<Flights tournament:{self.tournament.name} {self.start_at} - {self.end_at}>'

    def serialize(self, long=False):
        json = {
            "id": self.id,
            "tournament_id": self.tournament_id,
            "tournament": self.tournament.name,
            "start_at": self.start_at,
            "end_at": self.end_at,
            "day": self.day
        }
        if long:
            return {
                **json,
                "created_at": "",
                "updated_at": ""
            }
        return json



class Buy_ins(db.Model):
    __tablename__ = 'buy_ins'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'))
    receipt_img_url = db.Column(db.String(250))
    chips = db.Column(db.Integer)
    table = db.Column(db.Integer)
    seat = db.Column(db.Integer)
    place = db.Column(db.Integer)

    user = db.relationship('Profiles', back_populates='buy_ins')
    flight = db.relationship('Flights', back_populates='buy_ins')

    def __repr__(self):
        return f'<Buy_ins id:{self.id} user:{self.user_id} flight:{self.flight_id}>'

    @staticmethod
    def get_latest(user_id, tournament_id):
        return (Buy_ins.query
                        .filter( Buy_ins.flight.has( tournament_id=tournament_id ))
                        .filter_by( user_id=user_id )
                        .order_by( Buy_ins.id.desc() ).first())

    def serialize(self):
        u = self.user
        return {
            "id": self.id,
            "user_id": self.user_id,
            "flight_id": self.flight_id,
            "tournament_id": self.flight.tournament_id,
            "place": self.place,
            "chips": self.chips,
            "table": self.table,
            "seat": self.seat,
            "receipt_img_url": self.receipt_img_url,
            "user_name": u.nickname if u.nickname else f'{u.first_name} {u.last_name}'
        }



class Transactions(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    amount_in_coins = db.Column(db.Integer)
    amount_in_dollars = db.Column(db.Integer)

    user = db.relationship('Users', back_populates='transactions')

    def __repr__(self):
        return f'<Transactions user:{self.user.name} coins:{self.amount_in_coins} dollars:{self.amount_in_dollars}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "amount_in_coins": self.amount_in_coins,
            "amount_in_dollars": self.amount_in_dollars
        }



class Tokens(db.Model):
    __tablename__ = 'tokens'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    token = db.Column(db.String(256))
    expires_at = db.Column(db.DateTime)

    user = db.relationship('Users', back_populates='tokens')

    def __repr__(self):
        return f'<Tokens id:{self.id} user:{self.user_id}>'

    def serialize(self):
        return {
            "user_id": self.user_id,
            "token": self.token,
            "expires_at": self.expires_at
        }
