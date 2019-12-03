# from flask_sqlalchemy import SQLAlchemy
from models import db, Users, Profiles, Tournaments, Swaps, Flights, Buy_ins, Transactions, Coins
from datetime import datetime, timedelta
from utils import sha256

# db = SQLAlchemy('postgres://Francine@localhost/swapprofit')

def run_seeds():


    Coins.query.delete()
    Transactions.query.delete()
    Buy_ins.query.delete()
    Swaps.query.delete()
    Flights.query.delete()
    Tournaments.query.delete()
    Profiles.query.delete()
    Users.query.delete()


    lou = Users(
        email='lou@gmail.com',
        password=sha256('loustadler')
    )
    db.session.add(lou)
    lou = Profiles(
        first_name='Luiz', 
        last_name='Stadler',
        nickname='Lou',
        hendon_url='https://pokerdb.thehendonmob.com/player.php?a=r&n=207424',
        profile_pic_url='https://pokerdb.thehendonmob.com/pictures/Lou_Stadler_Winner.JPG',
        valid=True,
        user=lou
    )
    db.session.add(lou)

    cary = Users(
        email='katz234@gmail.com',
        password=sha256('carykatz')
    )
    db.session.add(cary)
    cary = Profiles(
        first_name='Cary', 
        last_name='Katz',
        nickname='',
        hendon_url='https://pokerdb.thehendonmob.com/player.php?a=r&n=26721',
        profile_pic_url='https://pokerdb.thehendonmob.com/pictures/carykatzpic.png',
        valid=True,
        user=cary
    )
    db.session.add(cary)

    kate = Users(
        email='hoang28974@gmail.com',
        password=sha256('kateHoang')
    )
    db.session.add(kate)
    kate = Profiles(
        first_name='Kate', 
        last_name='Hoang',
        nickname='',
        hendon_url='https://pokerdb.thehendonmob.com/player.php?a=r&n=421758',
        profile_pic_url='https://pokerdb.thehendonmob.com/pictures/Hoang_2.jpg',
        valid=True,
        user=kate
    )
    db.session.add(kate)

    nikita = Users(
        email='mikitapoker@gmail.com',
        password=sha256('nikitapoker')
    )
    db.session.add(nikita)
    nikita = Profiles(
        first_name='Nikita', 
        last_name='Bodyakovskiy',
        nickname='Mikita',
        hendon_url='https://pokerdb.thehendonmob.com/player.php?a=r&n=159100',
        profile_pic_url='https://pokerdb.thehendonmob.com/pictures/NikitaBadz18FRh.jpg',
        valid=True,
        user=nikita
    )
    db.session.add(nikita)

    heartland = Tournaments(
        name='Heartland Poker Tour - HPT Colorado, Black Hawk',
        address='261 Main St, Black Hawk, CO 80422',
        start_at=datetime(2019,10,11,12),
        end_at=datetime(2019,10,11,21)
    )
    db.session.add(heartland)

    stones = Tournaments(
        name='Stones Live Fall Poker Series',
        address='6510 Antelope Rd, Citrus Heights, CA 95621',
        start_at=datetime(2019,9,30,11),
        end_at=datetime(2019,10,1,22)
    )
    db.session.add(stones)

    wpt = Tournaments(
        name='WPT DeepStacks - WPTDS Sacramento',
        address='Thunder Valley Casino Resort, 1200 Athens Ave, Lincoln, CA 95648',
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

    db.session.add(Swaps(
        tournament=heartland,
        sender_user=lou,
        recipient_user=cary,
        percentage=10,
        winning_chips=None,
        due_at=(heartland.end_at + timedelta(days=4))
    ))

    db.session.add(Swaps(
        tournament=heartland,
        sender_user=cary,
        recipient_user=lou,
        percentage=10,
        winning_chips=None,
        due_at=(heartland.end_at + timedelta(days=4))
    ))

    db.session.add(Swaps(
        tournament=heartland,
        sender_user=nikita,
        recipient_user=kate,
        percentage=15,
        winning_chips=None,
        due_at=(heartland.end_at + timedelta(days=4))
    ))

    db.session.add(Swaps(
        tournament=heartland,
        sender_user=kate,
        recipient_user=nikita,
        percentage=15,
        winning_chips=None,
        due_at=(heartland.end_at + timedelta(days=4))
    ))

    db.session.add(Swaps(
        tournament=heartland,
        sender_user=lou,
        recipient_user=kate,
        percentage=5,
        winning_chips=None,
        due_at=(heartland.end_at + timedelta(days=4))
    ))

    db.session.add(Swaps(
        tournament=heartland,
        sender_user=kate,
        recipient_user=lou,
        percentage=5,
        winning_chips=None,
        due_at=(heartland.end_at + timedelta(days=4))
    ))

    db.session.add(Swaps(
        tournament=live,
        sender_user=lou,
        recipient_user=cary,
        percentage=10,
        winning_chips=None,
        due_at=(live.end_at + timedelta(days=4))
    ))

    db.session.add(Swaps(
        tournament=live,
        sender_user=cary,
        recipient_user=lou,
        percentage=10,
        winning_chips=None,
        due_at=(live.end_at + timedelta(days=4))
    ))

    db.session.add(Swaps(
        tournament=live,
        sender_user=nikita,
        recipient_user=kate,
        percentage=15,
        winning_chips=None,
        due_at=(live.end_at + timedelta(days=4))
    ))

    db.session.add(Swaps(
        tournament=live,
        sender_user=kate,
        recipient_user=nikita,
        percentage=15,
        winning_chips=None,
        due_at=(live.end_at + timedelta(days=4))
    ))

    db.session.add(Swaps(
        tournament=live,
        sender_user=lou,
        recipient_user=kate,
        percentage=5,
        winning_chips=None,
        due_at=(live.end_at + timedelta(days=4))
    ))

    db.session.add(Swaps(
        tournament=live,
        sender_user=kate,
        recipient_user=lou,
        percentage=5,
        winning_chips=None,
        due_at=(live.end_at + timedelta(days=4))
    ))

    db.session.add(Swaps(
        tournament=wpt,
        sender_user=lou,
        recipient_user=cary,
        percentage=10,
        winning_chips=10000,
        due_at=(wpt.end_at + timedelta(days=4))
    ))

    db.session.add(Swaps(
        tournament=wpt,
        sender_user=cary,
        recipient_user=lou,
        percentage=10,
        winning_chips=500,
        due_at=(wpt.end_at + timedelta(days=4))
    ))

    db.session.add(Swaps(
        tournament=wpt,
        sender_user=nikita,
        recipient_user=kate,
        percentage=15,
        winning_chips=100,
        due_at=(wpt.end_at + timedelta(days=4))
    ))

    db.session.add(Swaps(
        tournament=wpt,
        sender_user=kate,
        recipient_user=nikita,
        percentage=15,
        winning_chips=0,
        due_at=(wpt.end_at + timedelta(days=4))
    ))

    db.session.add(Swaps(
        tournament=wpt,
        sender_user=cary,
        recipient_user=kate,
        percentage=5,
        winning_chips=500,
        due_at=(wpt.end_at + timedelta(days=4))
    ))

    db.session.add(Swaps(
        tournament=wpt,
        sender_user=kate,
        recipient_user=cary,
        percentage=5,
        winning_chips=0,
        due_at=(wpt.end_at + timedelta(days=4))
    ))

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

    db.session.commit()