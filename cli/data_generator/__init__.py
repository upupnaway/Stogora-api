from random import choice

from fixtures import DESCRIPTIONS, TITLES, ZIP_CODES

def generate_stags():
    stags = []
    stags.append({
        'name': 'everything',
        'slug': '#everything',
        'stag_photo': "https://s3.amazonaws.com/stogora/stag_photos/everything.jpg"
    })
    stags.append({
        'name': 'ucberkeley',
        'slug': '#ucberkeley',
        'stag_photo': "http://hinshawsubdomain.dreamhosters.com/wp-content/uploads/2014/03/cropped-banner1.jpg"
    })
    stags.append({
        'name': 'bmw',
        'slug': '#bmw',
        'stag_photo': 'https://s3.amazonaws.com/stogora/stag_photos/f80.jpg'
    })
    stags.append({
        'name': 'concerts',
        'slug': '#concerts',
        'stag_photo': 'http://www.orltix.com/images-new/concert-banner.png'
    })
    return stags

def generate_users():
    users=[]
    users.append({
      'user_name': 'ray__mond',
      'first_name': 'Raymond',
      'last_name': 'Ma',
      'profile_photo': ("https://scontent.fsnc1-1.fna.fbcdn.net/hphotos-xft1/v/t1.0-9/11209747_10152847183228201_"
                        "1678818176835035994_n.jpg?oh=6c9c1918d717ae13c4d91922242ffda2&oe=568158FB"),
      'rating': 4,
      'points': 600,
      'email': 'raymondxma@gmail.com',
      'password': 'password'
    })
    users.append({
      'user_name': 'stpham92',
      'first_name': 'Steven',
      'last_name': 'Pham',
      'profile_photo': ("https://scontent.fsnc1-1.fna.fbcdn.net/hphotos-xpt1/t31.0-8/11921853_10153545108360396_"
                        "8388042826153936124_o.jpg"),
      'rating': 5,
      'points': 400,
      'email': 'stevenpham92@gmail.com',
      'password': 'password'
    })
    users.append({
      'user_name': 'ifilosemyself',
      'first_name': 'William',
      'last_name': 'Liow',
      'profile_photo': ("https://scontent.fsnc1-1.fna.fbcdn.net/hphotos-xpf1/v/t1.0-9/11011028_1107746029252179_7270897112"
                        "828497415_n.jpg?oh=a9ba856cfbb463af7c748750116d4a4e&oe=565D49D7"),
      'rating': 3,
      'points': 100,
      'email': 'william.liow92@gmail.com',
      'password': 'password'
    })

    return users

def generate_listings(user_model_instances, stag_instances):
    listings = []
    listings.append({
        'title': 'M3 M4 Matte Black Badge',
        'photo': 'https://s3.amazonaws.com/stogora/listing_photos/1.jpg',
        'price': 10,
        'quantity': 5,
        'user_id': choice(user_model_instances).id,
        'stag_id': 3,
        'subtitle': 'Only a few left! OEM Sizes',
        'description': '\n'.join(choice(DESCRIPTIONS)),
        'active': True,
        'sold': False
    })
    listings.append({
        'title': 'M3 M4 f82 Tow Hook Rope',
        'photo': 'https://s3.amazonaws.com/stogora/listing_photos/2.jpg',
        'price': 20,
        'quantity': 10,
        'user_id': choice(user_model_instances).id,
        'stag_id': 3,
        'subtitle': 'Multiple colors in stock!',
        'description': '\n'.join(choice(DESCRIPTIONS)),
        'active': True,
        'sold': False
    })
    listings.append({
        'title': 'Nikon D90 12.3 MP Camera',
        'photo': 'https://s3.amazonaws.com/stogora/listing_photos/3.jpg',
        'price': 800,
        'quantity': 1,
        'user_id': choice(user_model_instances).id,
        'stag_id': 2,
        'subtitle': 'Mint condition with extras',
        'description': '\n'.join(choice(DESCRIPTIONS)),
        'active': True,
        'sold': False
    })
    listings.append({
        'title': '1 hour photography session with professional touch-up',
        'photo': 'https://s3.amazonaws.com/stogora/listing_photos/4.jpg',
        'price': 30,
        'quantity': 100,
        'user_id': choice(user_model_instances).id,
        'stag_id': 2,
        'subtitle': 'willing to take pictures within 10 miles of berkeley',
        'description': '\n'.join(choice(DESCRIPTIONS)),
        'active': True,
        'sold': False
    })
    listings.append({
        'title': 'Brand New iPad Pro 64gb Black',
        'photo': 'https://s3.amazonaws.com/stogora/listing_photos/5.jpg',
        'price': 800,
        'quantity': 1,
        'user_id': choice(user_model_instances).id,
        'stag_id': 2,
        'subtitle': 'Brand New Still Sealed!!!',
        'description': '\n'.join(choice(DESCRIPTIONS)),
        'active': True,
        'sold': False
    })
    listings.append({
        'title': 'Used Sofa Stockholm by IKEA',
        'photo': 'https://s3.amazonaws.com/stogora/listing_photos/6.jpg',
        'price': 100,
        'quantity': 1,
        'user_id': choice(user_model_instances).id,
        'stag_id': 2,
        'subtitle': 'flawless comfy sofa sale!',
        'description': '\n'.join(choice(DESCRIPTIONS)),
        'active': True,
        'sold': False
    })
    listings.append({
        'title': 'Brand new Blender Bottles',
        'photo': 'https://s3.amazonaws.com/stogora/listing_photos/7.jpg',
        'price': 5,
        'quantity': 10,
        'user_id': choice(user_model_instances).id,
        'stag_id': 2,
        'subtitle': 'All Colors Available!',
        'description': '\n'.join(choice(DESCRIPTIONS)),
        'active': True,
        'sold': False
    })
    listings.append({
        'title': 'Taylor Swift Concert Ticket at UCLA',
        'photo': 'https://s3.amazonaws.com/stogora/listing_photos/8.jpg',
        'price': 300,
        'quantity': 1,
        'user_id': choice(user_model_instances).id,
        'stag_id': 4,
        'subtitle': 'Front Row Seat!',
        'description': '\n'.join(choice(DESCRIPTIONS)),
        'active': True,
        'sold': False
    })
    listings.append({
        'title': 'Xbox One Console Day One Edition',
        'photo': 'https://s3.amazonaws.com/stogora/listing_photos/9.jpg',
        'price': 400,
        'quantity': 1,
        'user_id': choice(user_model_instances).id,
        'stag_id': 2,
        'subtitle': 'Includes extra controller and 3 games',
        'description': '\n'.join(choice(DESCRIPTIONS)),
        'active': True,
        'sold': False
    })
    listings.append({
        'title': 'Wall Lamp by IKEA',
        'photo': 'https://s3.amazonaws.com/stogora/listing_photos/10.jpg',
        'price': 10,
        'quantity': 1,
        'user_id': choice(user_model_instances).id,
        'stag_id': 2,
        'subtitle': 'Brand new never installed',
        'description': '\n'.join(choice(DESCRIPTIONS)),
        'active': True,
        'sold': False
    })

    return listings



