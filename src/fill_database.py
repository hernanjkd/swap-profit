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

    
    db.session.commit()