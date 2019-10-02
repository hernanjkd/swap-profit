@app.route('/fill_database')
def fill_database():

    lou = Users(
        email='lou@gmail.com',
        password=hash('loustadler')
    )
    db.session.add(lou)
    lou = Profiles(
        first_name='Luiz', 
        last_name='Stadler',
        username='Lou',
        hendon_url='https://pokerdb.thehendonmob.com/player.php?a=r&n=207424',
        profile_picture_url='https://pokerdb.thehendonmob.com/pictures/Lou_Stadler_Winner.JPG',
        user=lou
    )
    db.session.add(lou)

    cary = Users(
        email='katz234@gmail.com',
        password=hash('carykatz')
    )
    db.session.add(cary)
    cary = Profiles(
        first_name='Cary', 
        last_name='Katz',
        username='',
        hendon_url='https://pokerdb.thehendonmob.com/player.php?a=r&n=26721',
        profile_picture_url='https://pokerdb.thehendonmob.com/pictures/carykatzpic.png',
        user=cary
    )
    db.session.add(cary)

    kate = Users(
        email='hoang28974@gmail.com',
        password=hash('kateHoang')
    )
    db.session.add(kate)
    kate = Profiles(
        first_name='Kate', 
        last_name='Hoang',
        username='',
        hendon_url='https://pokerdb.thehendonmob.com/player.php?a=r&n=421758',
        profile_picture_url='https://pokerdb.thehendonmob.com/pictures/Hoang_2.jpg',
        user=kate
    )
    db.session(kate)

    nikita = Users(
        email='mikitapoker@gmail.com',
        password=hash('nikitapoker')
    )
    db.session.add(nikita)
    nikita = Profiles(
        first_name='Nikita', 
        last_name='Bodyakovskiy',
        username='Mikita',
        hendon_url='https://pokerdb.thehendonmob.com/player.php?a=r&n=159100',
        profile_picture_url='https://pokerdb.thehendonmob.com/pictures/NikitaBadz18FRh.jpg',
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

    db.session.commit()

    