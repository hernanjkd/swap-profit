from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from models import (db, Users, Profiles, Tournaments, Flights, Swaps, Buy_ins,
    Transactions, Tournaments, Tokens)
# Flask and Flask-SQLAlchemy initialization here

def SetupAdmin(app):
    admin = Admin(app, name='Swapp App', template_mode='bootstrap3')
    admin.add_view(ModelView(Users, db.session))
    admin.add_view(ModelView(Profiles, db.session))
    admin.add_view(ModelView(Tournaments, db.session))
    admin.add_view(ModelView(Flights, db.session))
    admin.add_view(ModelView(Swaps, db.session))
    admin.add_view(ModelView(Buy_ins, db.session))
    admin.add_view(ModelView(Transactions, db.session))
    admin.add_view(ModelView(Tokens, db.session))



    return admin