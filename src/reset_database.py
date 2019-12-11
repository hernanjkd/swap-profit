# from flask_sqlalchemy import SQLAlchemy
from models import db, Users, Profiles, Tournaments, Swaps, Flights, Buy_ins, Transactions, Coins, Devices
from datetime import datetime, timedelta
from utils import sha256

# db = SQLAlchemy('postgres://Francine@localhost/swapprofit')

def run_seeds():


    Devices.query.delete()
    Coins.query.delete()
    Transactions.query.delete()
    Buy_ins.query.delete()
    Swaps.query.delete()
    Flights.query.delete()
    Tournaments.query.delete()
    Profiles.query.delete()
    Users.query.delete()

    ########################
    #  USERS AND PROFILES
    ########################

    lou = Users(
        email='lou@gmail.com',
        password=sha256('loustadler'),
        valid=True
    )
    db.session.add(lou)
    lou = Profiles(
        first_name='Luiz', 
        last_name='Stadler',
        nickname='Lou',
        hendon_url='https://pokerdb.thehendonmob.com/player.php?a=r&n=207424',
        profile_pic_url='https://pokerdb.thehendonmob.com/pictures/Lou_Stadler_Winner.JPG',
        user=lou
    )
    db.session.add(lou)

    cary = Users(
        email='katz234@gmail.com',
        password=sha256('carykatz'),
        valid=True
    )
    db.session.add(cary)
    cary = Profiles(
        first_name='Cary', 
        last_name='Katz',
        nickname='',
        hendon_url='https://pokerdb.thehendonmob.com/player.php?a=r&n=26721',
        profile_pic_url='https://pokerdb.thehendonmob.com/pictures/carykatzpic.png',
        user=cary
    )
    db.session.add(cary)

    kate = Users(
        email='hoang28974@gmail.com',
        password=sha256('kateHoang'),
        valid=True
    )
    db.session.add(kate)
    kate = Profiles(
        first_name='Kate', 
        last_name='Hoang',
        nickname='',
        hendon_url='https://pokerdb.thehendonmob.com/player.php?a=r&n=421758',
        profile_pic_url='https://pokerdb.thehendonmob.com/pictures/Hoang_2.jpg',
        user=kate
    )
    db.session.add(kate)

    nikita = Users(
        email='mikitapoker@gmail.com',
        password=sha256('nikitapoker'),
        valid=True
    )
    db.session.add(nikita)
    nikita = Profiles(
        first_name='Nikita', 
        last_name='Bodyakovskiy',
        nickname='Mikita',
        hendon_url='https://pokerdb.thehendonmob.com/player.php?a=r&n=159100',
        profile_pic_url='https://pokerdb.thehendonmob.com/pictures/NikitaBadz18FRh.jpg',
        user=nikita
    )
    db.session.add(nikita)

    ########################
    #     TOURNAMENTS
    ########################

    heartland = Tournaments(
        name='Heartland Poker Tour - HPT Colorado, Black Hawk',
        address='261 Main St',
        city='Black Hawk',
        state='CO',
        zip_code='80422',
        start_at=datetime(2019,10,11,12),
        end_at=datetime(2019,10,11,21)
    )
    db.session.add(heartland)

    stones = Tournaments(
        name='Stones Live Fall Poker Series',
        address='6510 Antelope Rd',
        city='Citrus Heights',
        state='CA',
        zip_code='95621',
        start_at=datetime(2019,9,30,11),
        end_at=datetime(2019,10,1,22)
    )
    db.session.add(stones)

    wpt = Tournaments(
        name='WPT DeepStacks - WPTDS Sacramento',
        address='Thunder Valley Casino Resort, 1200 Athens Ave',
        city='Lincoln',
        state='CA',
        zip_code='95648',
        start_at=datetime(2019,10,2,12),
        end_at=datetime(2019,10,2,22)
    )
    db.session.add(wpt)

    now = datetime.utcnow()
    live = Tournaments(
        name='Live Tournament at Vegas Casino',
        address='Thunder Valley Casino Resort, 1200 Athens Ave, Lincoln, CA 95648',
        start_at=now - timedelta(days=2),
        end_at=now + timedelta(days=600)
    )
    db.session.add(live)

    ########################
    #       FLIGHTS
    ########################

    flight1_live = Flights(
        start_at=now,
        end_at=now + timedelta(hours=5),
        tournament=live,
        day=1
    )
    db.session.add(flight1_live)

    flight2_live = Flights(
        start_at=now + timedelta(days=1),
        end_at=now + timedelta(days=1, hours=5),
        tournament=live,
        day=2
    )
    db.session.add(flight2_live)

    flight1_heartland = Flights(
        start_at=datetime(2019,10,11,12),
        end_at=datetime(2019,10,11,16),
        tournament=heartland,
        day=1
    )
    db.session.add(flight1_heartland)

    flight2_heartland = Flights(
        start_at=datetime(2019,10,11,16),
        end_at=datetime(2019,10,11,21),
        tournament=heartland,
        day=1
    )
    db.session.add(flight2_heartland)

    flight1_stones = Flights(
        start_at=datetime(2019,9,30,12),
        end_at=datetime(2019,9,30,15),
        tournament=stones,
        day=1
    )
    db.session.add(flight1_stones)

    flight2_stones = Flights(
        start_at=datetime(2019,9,30,15),
        end_at=datetime(2019,9,30,21),
        tournament=stones,
        day=1
    )
    db.session.add(flight2_stones)

    flight3_stones = Flights(
        start_at=datetime(2019,10,1,12),
        end_at=datetime(2019,10,1,21),
        tournament=stones,
        day=2
    )
    db.session.add(flight3_stones)

    flight1_wpt = Flights(
        start_at=datetime(2019,10,2,12),
        end_at=datetime(2019,10,2,22),
        tournament=wpt,
        day=1
    )
    db.session.add(flight1_wpt)

    ########################
    #        SWAPS
    ########################

    db.session.add(Swaps(
        tournament=heartland,
        sender_user=lou,
        recipient_user=cary,
        percentage=10,
        due_at=(heartland.end_at + timedelta(days=4))
    ))

    db.session.add(Swaps(
        tournament=heartland,
        sender_user=cary,
        recipient_user=lou,
        percentage=10,
        due_at=(heartland.end_at + timedelta(days=4))
    ))

    db.session.add(Swaps(
        tournament=heartland,
        sender_user=nikita,
        recipient_user=kate,
        percentage=15,
        due_at=(heartland.end_at + timedelta(days=4))
    ))

    db.session.add(Swaps(
        tournament=heartland,
        sender_user=kate,
        recipient_user=nikita,
        percentage=15,
        due_at=(heartland.end_at + timedelta(days=4))
    ))

    db.session.add(Swaps(
        tournament=heartland,
        sender_user=lou,
        recipient_user=kate,
        percentage=5,
        due_at=(heartland.end_at + timedelta(days=4))
    ))

    db.session.add(Swaps(
        tournament=heartland,
        sender_user=kate,
        recipient_user=lou,
        percentage=5,
        due_at=(heartland.end_at + timedelta(days=4))
    ))

    db.session.add(Swaps(
        tournament=live,
        sender_user=lou,
        recipient_user=cary,
        percentage=10,
        due_at=(live.end_at + timedelta(days=4))
    ))

    db.session.add(Swaps(
        tournament=live,
        sender_user=cary,
        recipient_user=lou,
        percentage=9,
        due_at=(live.end_at + timedelta(days=4))
    ))

    db.session.add(Swaps(
        tournament=live,
        sender_user=nikita,
        recipient_user=kate,
        percentage=15,
        due_at=(live.end_at + timedelta(days=4))
    ))

    db.session.add(Swaps(
        tournament=live,
        sender_user=kate,
        recipient_user=nikita,
        percentage=15,
        due_at=(live.end_at + timedelta(days=4))
    ))

    db.session.add(Swaps(
        tournament=live,
        sender_user=lou,
        recipient_user=kate,
        percentage=5,
        due_at=(live.end_at + timedelta(days=4))
    ))

    db.session.add(Swaps(
        tournament=live,
        sender_user=kate,
        recipient_user=lou,
        percentage=5,
        due_at=(live.end_at + timedelta(days=4))
    ))

    db.session.add(Swaps(
        tournament=wpt,
        sender_user=lou,
        recipient_user=cary,
        percentage=10,
        due_at=(wpt.end_at + timedelta(days=4))
    ))

    db.session.add(Swaps(
        tournament=wpt,
        sender_user=cary,
        recipient_user=lou,
        percentage=10,
        due_at=(wpt.end_at + timedelta(days=4))
    ))

    db.session.add(Swaps(
        tournament=wpt,
        sender_user=nikita,
        recipient_user=kate,
        percentage=15,
        due_at=(wpt.end_at + timedelta(days=4))
    ))

    db.session.add(Swaps(
        tournament=wpt,
        sender_user=kate,
        recipient_user=nikita,
        percentage=15,
        due_at=(wpt.end_at + timedelta(days=4))
    ))

    db.session.add(Swaps(
        tournament=wpt,
        sender_user=cary,
        recipient_user=kate,
        percentage=5,
        due_at=(wpt.end_at + timedelta(days=4))
    ))

    db.session.add(Swaps(
        tournament=wpt,
        sender_user=kate,
        recipient_user=cary,
        percentage=5,
        due_at=(wpt.end_at + timedelta(days=4))
    ))

    ########################
    #       BUY INS
    ########################

    db.session.add(Buy_ins(
        chips=1200,
        table=1,
        seat=2,
        user=lou,
        flight=flight1_live
    ))

    db.session.add(Buy_ins(
        chips=1200,
        table=1,
        seat=4,
        user=lou,
        flight=flight1_live
    ))

    db.session.add(Buy_ins(
        chips=500,
        table=7,
        seat=1,
        user=cary,
        flight=flight1_live
    ))

    db.session.add(Buy_ins(
        chips=500,
        table=3,
        seat=2,
        user=cary,
        flight=flight2_live
    ))

    db.session.add(Buy_ins(
        chips=1000,
        table=2,
        seat=2,
        user=kate,
        flight=flight2_live
    ))

    db.session.add(Buy_ins(
        chips=300,
        table=2,
        seat=2,
        user=kate,
        flight=flight2_live
    ))
    
    db.session.add(Buy_ins(
        chips=700,
        table=3,
        seat=1,
        user=nikita,
        flight=flight2_live
    ))

    ######################
    #   INCOMING SWAPS
    ######################

    db.session.add(Swaps(
        tournament=live,
        sender_user=kate,
        recipient_user=cary,
        percentage=10,
        due_at=(live.end_at + timedelta(days=4)),
        status='incoming'
    ))

    db.session.add(Swaps(
        tournament=live,
        sender_user=cary,
        recipient_user=kate,
        percentage=5,
        due_at=(live.end_at + timedelta(days=4)),
        status='pending'
    ))

    ####################################
    #   UPCOMING TOURNAMENT + FLIGHTS
    ####################################

    newvegas = Tournaments(
        name='New Vegas Strip - Texas Hold\'em Finale',
        address='129 East Fremont St.',
        city='Las Vegas',
        state='NV',
        zip_code='89101',
        start_at=datetime(2281,10,11,10),
        end_at=datetime(2281,10,11,22)
    )
    db.session.add(newvegas)

    flight1_newvegas = Flights(
        start_at=now + timedelta(days=1),
        end_at=now + timedelta(days=1, hours=5),
        tournament=newvegas,
        day=1
    )
    db.session.add(flight1_newvegas)

    flight2_newvegas = Flights(
        start_at=now + timedelta(days=1, hours=6),
        end_at=now + timedelta(days=1, hours=12),
        tournament=newvegas,
        day=1
    )
    db.session.add(flight2_newvegas)

    #######################
    #   UPCOMING BUYINS
    #######################
    
    db.session.add(Buy_ins(         
        chips=5000,         
        table=4,         
        seat=2,         
        user=lou,        
        flight=flight1_newvegas     
    ))

    db.session.add(Buy_ins(         
        chips=4000,         
        table=1,         
        seat=12,         
        user=cary,        
        flight=flight1_newvegas     
    ))

    db.session.add(Buy_ins(         
        chips=9000,         
        table=22,         
        seat=7,         
        user=lou,        
        flight=flight2_newvegas     
    ))

    db.session.add(Buy_ins(         
        chips=6000,         
        table=5,         
        seat=4,         
        user=nikita,        
        flight=flight2_newvegas     
    ))

    #####################
    #   AGREED SWAPS
    #####################

    db.session.add(Swaps(
        tournament=newvegas,
        sender_user=lou,
        recipient_user=cary,
        percentage=8,
        due_at=(newvegas.end_at + timedelta(days=4)),
        status='agreed'

    ))

    db.session.add(Swaps(
        tournament= newvegas,
        sender_user=cary,
        recipient_user=lou,
        percentage=2,
        due_at=(newvegas.end_at + timedelta(days=4))
    ))

    ######################
    #   REJECTED SWAPS
    ######################

    db.session.add(Swaps(
        tournament=newvegas,
        sender_user=lou,
        recipient_user=nikita,
        percentage=40,
        due_at=(newvegas.end_at + timedelta(days=4)),
        status='rejected'

    ))

    db.session.add(Swaps(
        tournament= newvegas,
        sender_user=nikita,
        recipient_user=lou,
        percentage=40,
        due_at=(newvegas.end_at + timedelta(days=4)),
        status='rejected'

    ))

    #####################
    #   CANCELED SWAPS
    #####################

    db.session.add(Swaps(
        tournament=live,
        sender_user=lou,
        recipient_user=nikita,
        percentage=20,
        due_at=(live.end_at + timedelta(days=4)),
	    status='canceled'
    ))

    db.session.add(Swaps(
        tournament= live,
        sender_user=nikita,
        recipient_user=lou,
        percentage=20,
        due_at=(live.end_at + timedelta(days=4)),
	    status='canceled'
    ))

    ######################
    #   PAST TOURNAMENT
    ######################

    oldvegas = Tournaments(
        name='Old Vegas Strip - Poker Eyes \'90',
        address='2211 N Rampart Blvd',
        city='Las Vegas',
        state='NV',
        zip_code='89145',
        start_at=datetime(1990,5,2,10),
        end_at=datetime(1990,5,2,15)
    )
    db.session.add(newvegas)

    flight1_oldvegas = Flights(
        start_at=now + timedelta(days=1),
        end_at=now + timedelta(days=1, hours=5),
        tournament=oldvegas,
        day=1
    )
    db.session.add(flight1_oldvegas)

    db.session.add(Buy_ins(         
        chips=7500,         
        table=14,         
        seat=12,         
        user=lou,        
        flight=flight1_oldvegas     
    ))

    db.session.add(Buy_ins(         
        chips=4500,         
        table=21,         
        seat=1,         
        user=cary,        
        flight=flight1_oldvegas     
    ))

    db.session.add(Swaps(
        tournament=oldvegas,
        sender_user=lou,
        recipient_user=cary,
        percentage=5,
        due_at=(oldvegas.end_at + timedelta(days=4)),
        status='agreed'
    ))

    db.session.add(Swaps(
        tournament= oldvegas,
        sender_user=cary,
        recipient_user=lou,
        percentage=7,
        due_at=(oldvegas.end_at + timedelta(days=4)),
        status='agreed'
    ))

    ##################
    # NEW TOURNAMENT
    ##################

    gamorrah = Tournaments(
            name='Final Days Poker at Gamorrah Casino',
            address='200 Fremont St, Las Vegas, NV 89101',
            start_at=datetime(2281,10,11,12),
            end_at=datetime(2281,10,11,21)
    )
    db.session.add(gamorrah)
    
    flight1_gamorrah = Flights(
            start_at=datetime(2281,10,11,12),
            end_at=datetime(2281,10,11,16),
            tournament=gamorrah,
            day=1
    )
    db.session.add(flight1_gamorrah)

    flight2_gamorrah = Flights(
            start_at=datetime(2281,10,11,16),
            end_at=datetime(2281,10,11,21),
            tournament=gamorrah,
            day=1
    )
    db.session.add(flight2_gamorrah)

    db.session.add(Buy_ins(
        chips=13000,
        table=13,
        seat=3,
        user=kate,
        flight=flight1_gamorrah
    ))

    db.session.commit()