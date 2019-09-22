from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=True, nullable=False)

    profile = db.relationship('Profiles', back_populates='user', uselist=False)
    transactions = db.relationship('Transactions', back_populates='user')
    tokens = db.relationship('Tokens', back_populates="user")

    def __repr__(self):
        return f'<Users {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "created_at": "",
            "updated_at": ""
        }



class Profiles(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100))
    hendon_url = db.Column(db.String(200))
    profile_picture_url = db.Column(db.String(250))

    user = db.relationship('Users', back_populates='profile', uselist=False)
    buy_ins = db.relationship('Buy_ins', back_populates='players')
    # sending_swaps = db.relationship('Swaps', back_populates='sender_user')
    # recieving_swaps = db.relationship('Swaps', back_populates='recipient_user)

    def __repr__(self):
        return f'<Profiles {self.first_name} {self.last_name}>'

    def serialize(self, long=False):
        json = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "email": self.user.email,
            "profile_picture_url": self.profile_picture_url
        }
        if long:
            return {
                **json,
                "hendon_url": self.hendon_url,
                "created_at": "",
                "updated_at": "",
                "swaps": list(map(lambda x: x.serialize(), self.recieving_swaps)),
                "buy_ins": list(map(lambda x: x.serialize(), self.buy_ins))
            }
        return json



class Tournaments(db.Model):
    __tablename__ = 'tournaments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    address = db.Column(db.String(250))
    start_at = db.Column(db.DateTime)
    end_at = db.Column(db.DateTime)

    flights = db.relationship('Flights', back_populates='tournament')
    swaps = db.relationship('Swaps', back_populates='tournament')

    def __repr__(self):
        return f'<Tournament {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "start_at": self.start_at,
            "end_at": self.end_at,
            "created_at": "",
            "updated_at": "",
            "flights": list(map(lambda x: x.serialize(), self.flights))
        }



class Flights(db.Model):
    __tablename__ = 'flights'
    id = db.Column(db.Integer, primary_key=True)
    start_at = db.Column(db.DateTime)
    end_at = db.Column(db.DateTime)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.id'))

    tournament = db.relationship('Tournaments', back_populates='flights')
    buy_ins = db.relationship('Buy_ins', back_populates='flights')

    def __repr__(self):
        return f'<Flights {self.tournament.name} {self.start_at} - {self.end_at}>'

    def serialize(self):
        return {
            "id": self.id,
            "tournament_id": self.tournament_id,
            "start_at": self.start_at,
            "end_at": self.end_at,
            "created_at": "",
            "updated_at": "",
            "buy_ins": list(map(lambda x: x.serialize(), self.buy_ins))
        }



class Swaps(db.Model):
    __tablename__ = 'swaps'
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.id'), primary_key=True)
    recipient_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('profiles.id') primary_key=True)
    percentage = db.Column(db.Integer, nullable=False)
    winning_chips = db.Column(db.Integer, default=None)
    due_at = db.Column(db.DateTime, default=None)

    tournament = db.relationship('Tournaments', back_populates='swaps')
    sender_user = db.relationship('Profiles', foreign_keys=[sender_id], backref='sending_swaps')
    recipient_user = db.relationship('Profiles', foreign_keys=[recipient_id], backref='reccieving_swaps')

    def __repr__(self):
        return f'<Swaps {self.user.email} {self.recipient_id} {self.tournament.name}>'

    def serialize(self, long=False):
        json = {
            "tournament_id": self.tournament_id,
            "recipient_user": self.recipient_user.serialize(),
            "percentage": self.percentage,
            "winning_chips": self.winning_chips,
            "due_at": self.due_at,
        }
        if long:
            return {
                **json,
                "sender_id": self.sender_id,
                "created_at": "",
                "updated_at": ""
            }
        return json


class Transactions(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    amount_in_coins = db.Column(db.Integer)
    amount_in_dollars = db.Column(db.Integer)

class Buy_ins(db.Model):
    __tablename__ = 'buy_ins'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'))
    receipt_image_url = db.Column(db.String(250))

class Tokens(db.Model):
    __tablename__ = 'tokens'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    token = db.Column(db.String(500))
    expires_at = db.Column(db.DateTime)

