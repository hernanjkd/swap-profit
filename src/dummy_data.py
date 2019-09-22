buy_ins = [
    {
        "id": 1,
        "user_id": 1,
        "flight_id": 1,
        "receipt_img_url": "http://lorempixel.com/400/200/",
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07"
    },
    {
        "id": 2,
        "user_id": 1,
        "flight_id": 1,
        "receipt_img_url": "http://lorempixel.com/400/200/",
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07"
    },
    {
        "id": 3,
        "user_id": 2,
        "flight_id": 1,
        "receipt_img_url": "http://lorempixel.com/400/200/",
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07"
    },
    {
        "id": 4,
        "user_id": 2,
        "flight_id": 2,
        "receipt_img_url": "http://lorempixel.com/400/200/",
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07"
    },
    {
        "id": 5,
        "user_id": 3,
        "flight_id": 1,
        "receipt_img_url": "http://lorempixel.com/400/200/",
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07"
    },
    {
        "id": 6,
        "user_id": 3,
        "flight_id": 3,
        "receipt_img_url": "http://lorempixel.com/400/200/",
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07"
    },
    {
        "id": 7,
        "user_id": 3,
        "flight_id": 4,
        "receipt_img_url": "http://lorempixel.com/400/200/",
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07"
    },
    {
        "id": 8,
        "user_id": 3,
        "flight_id": 5,
        "receipt_img_url": "http://lorempixel.com/400/200/",
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07"
    }
]

flights = [
    {
        "id": 1,
        "start_at": "Wed, 11 Oct 2019 16:00:00 GMT",
        "end_at": "Wed, 11 Oct 2019 21:00:00 GMT",
        "tournament_id": 1,
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07",
        "buy_ins": list(filter(lambda x: x['flight_id'] == 1, buy_ins))
    },
    {
        "id": 2,
        "start_at": "Wed, 11 Oct 2019 16:00:00 GMT",
        "end_at": "Wed, 11 Oct 2019 21:00:00 GMT",
        "tournament_id": 1,
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07",
        "buy_ins": list(filter(lambda x: x['flight_id'] == 2, buy_ins))
    },
    {
        "id": 3,
        "start_at": "Mon, 30 Sep 2019 12:00:00 GMT",
        "end_at": "Mon, 30 Sep 2019 21:00:00 GMT",
        "tournament_id": 2,
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07",
        "buy_ins": list(filter(lambda x: x['flight_id'] == 3, buy_ins))
    },
    {
        "id": 4,
        "start_at": "Tue, 1 Oct 2019 12:00:00 GMT",
        "end_at": "Tue, 1 Oct 2019 21:00:00 GMT",
        "tournament_id": 2,
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07",
        "buy_ins": list(filter(lambda x: x['flight_id'] == 4, buy_ins))
    },
    {
        "id": 5,
        "start_at": "Wed, 11 Oct 2019 12:00:00 GMT",
        "end_at": "Wed, 11 Oct 2019 16:00:00 GMT",
        "tournament_id": 3,
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07",
        "buy_ins": list(filter(lambda x: x['flight_id'] == 5, buy_ins))
    },
]

swaps = [
    {
        "tournament_id": 1,
        "sender_id": 1,
        "recipient_id": 2,
        "percentage": 5,
        "winning_chips": None, # these will be null while they are playing
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07"
    },
    {
        "tournament_id": 1,
        "sender_id": 2,
        "recipient_id": 1,
        "percentage": 5,
        "winning_chips": None, # these will be null while they are playing
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07"
    },
    {
        "tournament_id": 1,
        "sender_id": 2,
        "recipient_id": 3,
        "percentage": 10,
        "winning_chips": None, # these will be null while they are playing
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07"
    },
    {
        "tournament_id": 1,
        "sender_id": 3,
        "recipient_id": 2,
        "percentage": 10,
        "winning_chips": None, # these will be null while they are playing
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07"
    },
    {
        "tournament_id": 2,
        "sender_id": 1,
        "recipient_id": 3,
        "percentage": 12,
        "winning_chips": None, # these will be null while they are playing
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07"
    },
    {
        "tournament_id": 2,
        "sender_id": 3,
        "recipient_id": 1,
        "percentage": 12,
        "winning_chips": None, # these will be null while they are playing
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07"
    },
    {
        "tournament_id": 2,
        "sender_id": 2,
        "recipient_id": 1,
        "percentage": 3,
        "winning_chips": 1000,
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07"
    },
    {
        "tournament_id": 2,
        "sender_id": 1,
        "recipient_id": 2,
        "percentage": 3,
        "winning_chips": 300,
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07"
    },
    {
        "tournament_id": 3,
        "sender_id": 2,
        "recipient_id": 3,
        "percentage": 20,
        "winning_chips": 500,
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07"
    },
    {
        "tournament_id": 3,
        "sender_id": 3,
        "recipient_id": 2,
        "percentage": 20,
        "winning_chips": 0,
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07"
    },
    {
        "tournament_id": 3,
        "sender_id": 1,
        "recipient_id": 3,
        "percentage": 16,
        "winning_chips": 500,
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07"
    },
    {
        "tournament_id": 3,
        "sender_id": 3,
        "recipient_id": 1,
        "percentage": 16,
        "winning_chips": 600,
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07"
    }
]

profiles = [
    {
        "id": 1,
        "first_name": "Cary",
        "last_name": "Katz",
        "username": "",
        "email": "katz234@gmail.com",
        "hendon_url": "https://pokerdb.thehendonmob.com/player.php?a=r&n=26721",
        "profile_picture_url": "https://pokerdb.thehendonmob.com/pictures/carykatzpic.png",
        "transactions": "list of transactions",
        "created_at": "Tue, 17 Sep 2019 04:23:59 GMT",
        "updated_at": "Tue, 17 Sep 2019 04:23:59 GMT",
        "tokens": 12,
        "swaps": list(filter(lambda x: x['sender_id'] == 1, swaps)),
        "buy_ins": list(filter(lambda x: x['user_id'] == 1, buy_ins))
    },
    {
        "id": 2,
        "first_name": "Kate",
        "last_name": "Hoang",
        "username": "",
        "email": "hoang234@gmail.com",
        "hendon_url": "https://pokerdb.thehendonmob.com/player.php?a=r&n=421758",
        "profile_picture_url": "https://pokerdb.thehendonmob.com/pictures/Hoang_2.jpg",
        "transactions": "list of transactions",
        "created_at": "Tue, 17 Sep 2019 04:23:59 GMT",
        "updated_at": "Tue, 17 Sep 2019 04:23:59 GMT",
        "tokens": 0,
        "swaps": list(filter(lambda x: x['sender_id'] == 2, swaps)),
        "buy_ins": list(filter(lambda x: x['flight_id'] == 2, buy_ins))
    },
    {
        "id": 3,
        "first_name": "Nikita",
        "last_name": "Bodyakovskiy",
        "username": "Mikita",
        "email": "bodyakov@gmail.com",
        "hendon_url": "https://pokerdb.thehendonmob.com/player.php?a=r&n=159100",
        "profile_picture_url": "https://pokerdb.thehendonmob.com/pictures/NikitaBadz18FRh.jpg",
        "transactions": "list of transactions",
        "created_at": "Tue, 17 Sep 2019 04:23:59 GMT",
        "updated_at": "Tue, 17 Sep 2019 04:23:59 GMT",
        "tokens": 5,
        "swaps": list(filter(lambda x: x['sender_id'] == 3, swaps)),
        "buy_ins": list(filter(lambda x: x['flight_id'] == 3, buy_ins))
    }
]

tournaments = [
    {
        "id": 1,
        "name": "Heartland Poker Tour - HPT Colorado, Black Hawk",
        "address": "261 Main St, Black Hawk, CO 80422",
        "start_at": "Wed, 11 Oct 2019 12:00:00 GMT",
        "end_at": "Wed, 11 Oct 2019 21:00:00 GMT",
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07",
        "swaps": "should we put a list of all the swaps for the tournament?",
        "flights": list(filter(lambda x: x['tournament_id'] == 1, flights))
    },
    {
        "id": 2,
        "name": "Stones Live Fall Poker Series",
        "address": "6510 Antelope Rd, Citrus Heights, CA 95621",
        "start_at": "Mon, 30 Sep 2019 11:00:00 GMT",
        "end_at": "Tue, 1 Oct 2019 22:00:00 GMT",
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07",
        "swaps": "should we put a list of all the swaps for the tournament?",
        "flights": list(filter(lambda x: x['tournament_id'] == 2, flights))
    },
    {
        "id": 3,
        "name": "WPT DeepStacks - WPTDS Sacramento",
        "address": "Thunder Valley Casino Resort, 1200 Athens Ave, Lincoln, CA 95648",
        "start_at": "Wed, 2 Oct 2019 12:00:00 GMT",
        "end_at": "Wed, 2 Oct 2019 21:00:00 GMT",
        "created_at": "Mon, 16 Sep 2019, 14:55:32",
        "updated_at": "Tue, 17 Sep 2019, 22:44:07",
        "swaps": "should we put a list of all the swaps for the tournament?",
        "flights": list(filter(lambda x: x['tournament_id'] == 3, flights))
    }
]