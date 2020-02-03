import os
import models as m
from models import db
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Table, MetaData



engine = create_engine('postgres://Francine@localhost/swapprofit')

metadata = MetaData()
# connection = engine.connect()

# users = Table('users', metadata, autoload=True, autoload_with=engine)

m.Users.query.get(1)

print( repr(users) )


