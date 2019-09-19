from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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
            "created_at": "",
            "updated_at": "",
            "email": self.email
        }



class Profiles(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100))
    hendon_url = db.Column(db.String(200))
    profile_picture_url = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('Users', back_populates='profile', uselist=False)
    swaps = db.relationship('Swaps', back_populates='user')
    buy_ins = db.relationship('Buy_ins', back_populates='user')

    def __repr__(self):
        return f'<Profiles {self.first_name} {self.last_name}>'

    def serialize(self):
        return {
            "id": self.id,
            "date_created": self.date_created,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.user.email,
            "flights": list(map(lambda x: x.serialize(), self.flights))
        }



class Tournaments(db.Model):
    __tablename__ = 'tournaments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    flights = db.relationship('Flights', back_populates='tournament')

    def __repr__(self):
        return f'<Tournament {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "date_created": self.date_created,
            "name": self.name,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "flights": list(map(lambda x: x.serialize(), self.flights))
        }



class Flights(db.Model):
    __tablename__ = 'flights'
    id = db.Column(db.Integer, primary_key=True)

#     start_date = db.Column(db.Date)
#     end_date = db.Column(db.Date)

#     tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.id'))
#     tournament = db.relationship('Tournaments', back_populates='flights')

    
#     def __repr__(self):
#         return f'<Flights {self.tournament.name} {self.start_date} - {self.end_date}>'

#     def serialize(self):
#         return {
#             "id": self.id,
#             "date_created": self.date_created,
#             "start_date": self.start_date,
#             "end_date": self.end_date,
#             "players": list(map(lambda x: x.serialize(), self.players))
#         }





class Swaps(db.Model):
    __tablename__ = 'swaps'
    id = db.Column(db.Integer, primary_key=True)

#     amount_percentage = db.Column(db.Integer)
#     completed = db.Column(db.Boolean, default=False)

#     sender_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
#     reciever_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
#     tournament_id = db.Column(db.Integer, db.ForeignKey('Tournaments.id'))

#     def __repr__(self):
#         return f'<Swaps {self.id}>'

#     def serialize(self):
#         return {
#             "id": self.id,
#             "amount_percentage": self.amount_percentage,
#             "completed": self.completed
#             # "sender": 
#             # "reciever": 
#             # "tournament": 
#         }


class Transactions(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
#     amount = db.Column(db.Integer)

#     user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))


class Buy_ins(db.Model):
    __tablename__ = 'buy_ins'
    id = db.Column(db.Integer, primary_key=True)

class Tokens(db.Model):
    __tablename__ = 'tokens'
    id = db.Column(db.Integer, primary_key=True)

