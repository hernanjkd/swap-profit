from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=True, nullable=False)

    profile = db.relationship('Profiles', back_populates='user', uselist=False)
    transactions = db.relationship('Transactions', back_populates='user')
    tokens = db.relationship('Tokens', back_populates='user')

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
    buy_ins = db.relationship('Buy_ins', back_populates='user')
    # sending_swaps = db.relationship('Swaps', back_populates='sender_user')
    # receiving_swaps = db.relationship('Swaps', back_populates='recipient_user)

    def __repr__(self):
        return f'<Profiles {self.first_name} {self.last_name}>'

    def serialize(self, long=False):
        # r = {x['id']: x.serialize() for x in self.receiving_swaps}
        # lst = [{**x.serialize(sender=True), **r[x['id']]} for x in self.sending_swaps]

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
                # "swaps": lst,
                "receiving_swaps": [x.serialize() for x in self.receiving_swaps],
                # "receiving_swaps": list(map(lambda x: x.serialize(), self.receiving_swaps)),
                # "sending_swaps": list(map(lambda x: x.serialize(sender=True), self.sending_swaps)),
                "buy_ins": [x.serialize(flight=True) for x in self.buy_ins]
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
            "flights": [x.serialize() for x in self.flights]
        }



class Flights(db.Model):
    __tablename__ = 'flights'
    id = db.Column(db.Integer, primary_key=True)
    start_at = db.Column(db.DateTime)
    end_at = db.Column(db.DateTime)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.id'))

    tournament = db.relationship('Tournaments', back_populates='flights')
    buy_ins = db.relationship('Buy_ins', back_populates='flight')

    def __repr__(self):
        return f'<Flights {self.tournament.name} {self.start_at} - {self.end_at}>'

    def serialize(self, long=False):
        json = {
            "id": self.id,
            "tournament": self.tournament.name,
            "start_at": self.start_at,
            "end_at": self.end_at
        }
        if long:
            return {
                **json,
                "tournament_id": self.tournament_id,
                "created_at": "",
                "updated_at": "",
                "buy_ins": [x.serialize(user=True) for x in self.buy_ins]
            }
        return json



class Swaps(db.Model):
    __tablename__ = 'swaps'
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.id'), primary_key=True)
    recipient_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), primary_key=True)
    percentage = db.Column(db.Integer, nullable=False)
    winning_chips = db.Column(db.Integer, default=None)
    due_at = db.Column(db.DateTime, default=None)

    tournament = db.relationship('Tournaments', back_populates='swaps')
    sender_user = db.relationship('Profiles', foreign_keys=[sender_id], backref='sending_swaps')
    recipient_user = db.relationship('Profiles', foreign_keys=[recipient_id], backref='receiving_swaps')

    def __repr__(self):
        return f'<Swaps {self.user.email} {self.recipient_id} {self.tournament.name}>'

    def serialize(self, long=False, sender=False):
        json = {
            "sender_id": self.sender_id,
            "tournament_id": self.tournament_id,
            "percentage": self.percentage,
            "winning_chips": self.winning_chips,
            "due_at": self.due_at,
            "user": self.sender_user.serialize()
        }
        if sender:
            return {
                "recipient_id": self.recipient_id,
                "tournament_id": self.tournament_id,
                "due_at": self.due_at,
                "winning_chips": self.winning_chips
            }
        if long:
            return {
                **json,
                "recipient_id": self.recipient_id,
                "created_at": "",
                "updated_at": ""
            }
        return json



class Buy_ins(db.Model):
    __tablename__ = 'buy_ins'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'))
    receipt_image_url = db.Column(db.String(250))

    user = db.relationship('Profiles', back_populates='buy_ins')
    flight = db.relationship('Flights', back_populates='buy_ins')

    def __repr__(self):
        return f'<Buy_ins {self.id} {self.user_id} {self.flight_id}>'

    def serialize(self, user=False, flight=False):
        if user:
            return {
                "id": self.id,
                "user": self.user.serialize()
            }
        if flight:
            return {
                "id": self.id,
                "flight": self.flight.serialize()
            }
        return {
            "id": self.id,
            "user_id": self.user_id,
            "flight_id": self.flight_id,
            "receipt_image_url": self.receipt_image_url
        }



class Transactions(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    amount_in_coins = db.Column(db.Integer)
    amount_in_dollars = db.Column(db.Integer)

    user = db.relationship('Users', back_populates='transactions')

    def __repr__(self):
        return f'<Transactions {self.user.name} {self.amount_in_coins} {self.amount_in_dollars}>'

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
    token = db.Column(db.String(500))
    expires_at = db.Column(db.DateTime)

    user = db.relationship('Users', back_populates='tokens')

    def __repr__(self):
        return f'<Tokens {self.token}>'

    def serialize(self):
        return {
            "user_id": self.user_id,
            "token": self.token,
            "expires_at": self.expires_at
        }
