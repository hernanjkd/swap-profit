import os
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models import Tournaments, Flights
from datetime import datetime, timedelta


engine = create_engine( os.environ.get('DATABASE_URL'))
Session = sessionmaker( bind=engine )
session = Session()

time = datetime.utcnow() + timedelta(days=1)
trmnt = session.query(Tournaments) \
    .filter( func.max(Tournaments.id) )
x = [z for z in trmnt]
print(x)
# trmnts = session.query(Tournaments) \
    # .filter_by(name='New Vegas Strip - Texas Hold\'em Finale') \
    # .filter( Tournaments.flights.any(
    #     func.max(Flights.start_at) < time
    # ))


# _17hrs_ago = datetime.utcnow() - timedelta(hours=17)
# trmnts = session.query(Tournaments) \
#             .filter( Tournaments.status == 'open')
#             .where( Tournaments.flights.any( 
#                 func.max(Flights.start_at) < _17hrs_ago ))
            # .filter( Tournaments.flights)

