from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, desc
from datetime import datetime

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    valid = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    profile = db.relationship('Profiles', back_populates='user', uselist=False)
    transactions = db.relationship('Transactions', back_populates='user')
    coins = db.relationship('Coins', back_populates='user')
    devices = db.relationship('Devices', back_populates='user')

    def __repr__(self):
        return f'<Users {self.email}>'

    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'valid': self.valid,
            'created_at': self.created_at,
            'updated_at': self.updated_at
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
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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

    def serialize(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'nickname': self.nickname,
            'email': self.user.email,
            'profile_pic_url': self.profile_pic_url,
            'hendon_url': self.hendon_url,
            'roi': self.roi,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }



class Swaps(db.Model):
    __tablename__ = 'swaps'
    sender_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), primary_key=True)
    recipient_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.id'), primary_key=True)
    percentage = db.Column(db.Integer, nullable=False)
    due_at = db.Column(db.DateTime, default=None)
    paid = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    valid_status = ['pending','rejected','agreed','canceled','incoming']
    status = db.Column(db.String(20), default='pending')

    tournament = db.relationship('Tournaments', back_populates='swaps')
    sender_user = db.relationship('Profiles', foreign_keys=[sender_id], backref='sending_swaps')
    recipient_user = db.relationship('Profiles', foreign_keys=[recipient_id], backref='receiving_swaps')

    def __init__(self, **kwargs):
        for attr, value in kwargs.items():
            if not hasattr(self, attr):
                raise Exception(f"'{attr}' is an invalid keyword argument for Swaps")
            if attr == 'valid_status':
                raise Exception(f"'{attr}' can not be modified")
            if attr == 'status':               
                if value not in self.valid_status:
                    raise Exception(f"'{value}' is an invalid status for Swaps")
            setattr(self, attr, value)

    def __repr__(self):
        return (f'<Swaps sender_email:{self.sender_user.user.email} ' 
            + f'recipient_email:{self.recipient_user.user.email} '
            + f'tournament:{self.tournament.name}>')

    def get_counter_percentage(self):
        ids = (self.recipient_id, self.sender_id, self.tournament_id)
        swap = Swaps.query.get(ids)
        return swap.percentage

    def serialize(self):
        return {
            'tournament_id': self.tournament_id,
            'percentage': self.percentage,
            'counter_percentage': self.get_counter_percentage(),
            'due_at': self.due_at,
            'status': self.status,
            'sender_user': self.sender_user.serialize(),
            'recipient_user': self.recipient_user.serialize(),
            'paid': self.paid,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }



class Tournaments(db.Model):
    __tablename__ = 'tournaments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    address = db.Column(db.String(200))
    city = db.Column(db.String(50))
    state = db.Column(db.String(20))
    zip_code = db.Column(db.String(14))
    start_at = db.Column(db.DateTime)
    end_at = db.Column(db.DateTime)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    flights = db.relationship('Flights', back_populates='tournament')
    swaps = db.relationship('Swaps', back_populates='tournament')

    def __repr__(self):
        return f'<Tournament {self.name}>'

    @staticmethod
    def get_live_upcoming(user_id):
        now = datetime.utcnow()
        trmnts = (Tournaments.query
                    .filter( Tournaments.end_at > now )
                    .filter( Tournaments.flights.any( 
                        Flights.buy_ins.any( user_id = user_id )))
                    .order_by( Tournaments.start_at.asc() ))
        return trmnts if trmnts.count() > 0 else None

    def get_all_users_latest_buyins(self):
        all_buyins = Buy_ins.query.filter( 
                        Buy_ins.flight.has( 
                            Flights.tournament_id == self.id ))
        user_ids = []
        buyins = []
        for buyin in all_buyins:
            user_id = buyin.user_id
            # Users may have multiple buy_ins in one tournament
            if user_id not in user_ids:
                user_ids.append( user_id )
                buyins.append( Buy_ins.get_latest(user_id, self.id).serialize() )
        return buyins

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'start_at': self.start_at,
            'end_at': self.end_at,
            'longitude': self.longitude,
            'latitude': self.latitude,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'flights': [x.serialize() for x in self.flights],
            'buy_ins': self.get_all_users_latest_buyins()
        }



class Flights(db.Model):
    __tablename__ = 'flights'
    id = db.Column(db.Integer, primary_key=True)
    start_at = db.Column(db.DateTime)
    end_at = db.Column(db.DateTime)
    day = db.Column(db.Integer)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tournament = db.relationship('Tournaments', back_populates='flights')
    buy_ins = db.relationship('Buy_ins', back_populates='flight')

    def __repr__(self):
        return f'<Flights tournament:{self.tournament.name} {self.start_at} - {self.end_at}>'

    def serialize(self):
        return {
            'id': self.id,
            'tournament_id': self.tournament_id,
            'tournament': self.tournament.name,
            'start_at': self.start_at,
            'end_at': self.end_at,
            'day': self.day,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }



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
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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
            'id': self.id,
            'user_id': self.user_id,
            'flight_id': self.flight_id,
            'tournament_id': self.flight.tournament_id,
            'place': self.place,
            'chips': self.chips,
            'table': self.table,
            'seat': self.seat,
            'receipt_img_url': self.receipt_img_url,
            'user_name': u.nickname if u.nickname else f'{u.first_name} {u.last_name}',
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }



class Transactions(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    amount_in_coins = db.Column(db.Integer)
    amount_in_dollars = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('Users', back_populates='transactions')

    def __repr__(self):
        return f'<Transactions user:{self.user.name} coins:{self.amount_in_coins} dollars:{self.amount_in_dollars}>'

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'amount_in_coins': self.amount_in_coins,
            'amount_in_dollars': self.amount_in_dollars,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }



class Coins(db.Model):
    __tablename__ = 'coins'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    token = db.Column(db.String(256))
    expires_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('Users', back_populates='coins')

    def __repr__(self):
        return f'<Coins id:{self.id} user:{self.user_id}>'

    def serialize(self):
        return {
            'user_id': self.user_id,
            'token': self.token,
            'expires_at': self.expires_at,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }



class Devices(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    token = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('Users', back_populates='devices')

    def __repr__(self):
        return f'<Devices id:{self.id} user_email:{self.user.email}>'

    def serialize(self):
        return {
            'id': self.id,
            'token': self.token,
            'user_id': self.user_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }



class Zip_Codes(db.Model):
    __tablename__ = 'zip_codes'
    id = db.Column(db.Integer, primary_key=True)
    zip_code = db.Column(db.String(14))
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Zip_Codes {self.zip_code}>'

    def serialize(self):
        return {
            'id': self.id,
            'zip_code': self.zip_code,
            'longitude': self.longitude,
            'latitude': self.latitude,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }