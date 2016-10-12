from datetime import datetime, timedelta
import random
from uuid import uuid4

from flask import Flask, g, jsonify, render_template, request, session
from flask.ext.cors import CORS, cross_origin
from flask.ext.login import current_user, LoginManager, login_required, login_user, logout_user
from flask.ext.sqlalchemy import SQLAlchemy
from stogora_app import config
from stogora_app.utils import timestamp

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
cors = CORS(app, origins='http://localhost:4200/*', allow_headers='Content-Type', supports_credentials=True)
app.secret_key = '?\x8eP\x80\xd5\x83\xc6/5z\xcf\xfbGy\xb6O\x02\x1c\xcc$\xe9Z\xea\x95'
login_manager = LoginManager()
login_manager.init_app(app)

from stogora_app.beta.routes import betas
from stogora_app.models.beta import Beta
from stogora_app.address.routes import address_bp
from stogora_app.authentication.routes import authentication, fb_register, get_user_info
from stogora_app.following.routes import following_bp
from stogora_app.listing.routes import listings_bp
from stogora_app.listing.comments.routes import listing_comment_bp
from stogora_app.models.users import User
from stogora_app.messages.routes import message_thread_bp
from stogora_app.user.routes import users_bp
from stogora_app.search.routes import search_bp
from stogora_app.stag.routes import stags_bp
from stogora_app.models.listings import Listing
from stogora_app.models.photos import Photos

app.register_blueprint(betas, url_prefix='/beta')
app.register_blueprint(address_bp, url_prefix='/addresses')
app.register_blueprint(authentication, url_prefix='/user')
app.register_blueprint(listings_bp, url_prefix='/listings')
app.register_blueprint(listing_comment_bp, url_prefix='/listing-comments')
app.register_blueprint(search_bp, url_prefix='/search')
app.register_blueprint(stags_bp, url_prefix='/stags')
app.register_blueprint(message_thread_bp, url_prefix='/messages')
app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(following_bp, url_prefix='/followings')

# Log production issues
if app.debug is not True:
  import logging
  from logging import StreamHandler

  file_handler = StreamHandler()
  file_handler.setLevel(logging.ERROR)
  app.logger.setLevel(logging.ERROR)
  app.logger.addHandler(file_handler)


@login_manager.user_loader
def load_user(user_id):
  return User.get_by_id(user_id)


@app.before_request
def inject_csrf_token():
  if '_csrf' not in session or session.get('_csrf') is None:
    session['_csrf'] = uuid4().hex


@app.after_request
def add_security_headers(response):
  """
  Add security params in the headers
  """
  response.headers.add('X-Frame-Options', 'DENY')
  response.headers.add('X-XSS-Protection', '1; mode=block')
  response.headers.add('X-Content-Type-Options', 'nosniff')
  response.cache_control.max_age = 300
  return response


@app.route('/')
def index():
  return render_template('layout.html', stuff=uuid4())


@app.route('/messageThreads')
def message_threads():
  threads = [{
    'id': 1,  # IDs match database user id
    'username': 'stpham',
    'name': 'Steven Pham',
    'userImageUrl': 'https://scontent-lga3-1.xx.fbcdn.net/hphotos-xpt1/t31.0-8/11921853_10153545108360396_8388042826153936124_o.jpg',
    'lastMessaged': timestamp(datetime.now() - timedelta(hours=int(random.random() * 10))),
    'lastMessageBlurb': 'Blah blah Blah blah Blah blah Blah blah Blah blah Blah blah ',
  }, {
    'id': 2,
    'username': 'raymondxma',
    'name': 'Raymond Ma',
    'userImageUrl': 'https://scontent-lga3-1.xx.fbcdn.net/hphotos-xpt1/t31.0-8/11921853_10153545108360396_8388042826153936124_o.jpg',
    'lastMessaged': timestamp(datetime.now() - timedelta(hours=int(random.random() * 10))),
    'lastMessageBlurb': 'Blah blah Blah blah Blah blah Blah blah Blah blah Blah blah ',
  }, {
    'id': 3,
    'username': 'lol',
    'name': 'SLumsy',
    'userImageUrl': 'https://scontent-lga3-1.xx.fbcdn.net/hphotos-xpt1/t31.0-8/11921853_10153545108360396_8388042826153936124_o.jpg',
    'lastMessaged': timestamp(datetime.now() - timedelta(hours=int(random.random() * 10))),
    'lastMessageBlurb': 'Blah blah Blah blah Blah blah Blah blah Blah blah Blah blah ',
  }]
  return jsonify({'messageThreads': threads})


@app.route('/notifications')
def notifications():
  notifications_items = [{
    'id': 1,
    'type': 'message',
    'sender': 'Johnny Cage',
    'body': 'Johnny sent you a message',
    'timestamp': timestamp(datetime.now() - timedelta(hours=3))
  }, {
    'id': 2,
    'type': 'comment',
    'body': 'You have a new comment',
    'threadTitle': 'Used Nikon D90 12.3 MP Camera',
    'stag': 'photogear',
    'timestamp': timestamp(datetime.now() - timedelta(days=3))
  }, {
    'id': 3,
    'type': 'comment',
    'body': 'You have a new comment',
    'threadTitle': 'M3 M4 Matte Black Badge',
    'stag': 'bmwm4',
    'timestamp': timestamp(datetime.now() - timedelta(days=3))
  }]

  notifications_items.append({
    'id': int(random.random() * 1000),
    'type': 'comment',
    'body': 'You have a new comment',
    'threadTitle': 'M3 M4 Matte Black Badge',
    'stag': 'bmwm4',
    'timestamp': timestamp(datetime.now() - timedelta(days=3))
  })

  return jsonify({'notifications': notifications_items})

@app.route('/comments')
def comments():
  comment_list = [{
    'id': 'p1',
    'thread': 't1',
    'authorId': '3',
    'userName': 'ifilosemyself',
    'upvotes': 5,
    'profilePhoto': ("https://scontent.fsnc1-1.fna.fbcdn.net/hphotos-xpf1/v/t1.0-9/11011028_1107746029252179_7270897112"
                     "828497415_n.jpg?oh=a9ba856cfbb463af7c748750116d4a4e&oe=565D49D7"),
    'datePosted': 1433660400000,
    'comment': '@ray__mond These will fit the 2014 m3 and m4s? Will this also fit the 2008-2012 m3s?'
  }, {
    'id': 'p2',
    'thread': 't1',
    'authorId': '1',
    'userName': 'ray__mond',
    'upvotes': 0,
    'profilePhoto': ("https://scontent.fsnc1-1.fna.fbcdn.net/hphotos-xft1/v/t1.0-9/11209747_10152847183228201_"
                     "1678818176835035994_n.jpg?oh=6c9c1918d717ae13c4d91922242ffda2&oe=568158FB"),
    'datePosted': 1433660400000,
    'comment': '@ifilosemyself it sure will! It will fit all m3 - m4 from 2008 onwards'
  }, {
    'id': 'p3',
    'thread': 't1',
    'authorId': '3',
    'userName': 'ifilosemyself',
    'upvotes': 2,
    'profilePhoto': ("https://scontent.fsnc1-1.fna.fbcdn.net/hphotos-xpf1/v/t1.0-9/11011028_1107746029252179_7270897112"
                     "828497415_n.jpg?oh=a9ba856cfbb463af7c748750116d4a4e&oe=565D49D7"),
    'datePosted': 1433660400000,
    'comment': '@ray_mond any discounts if I buy in bulk?'
  }]
  return jsonify({'comments': comment_list})


@app.route('/login', methods=['POST'])
def login():
  """
  POST route for logging in traditionally. First checks if user exists in the data base via email then checks if the
  passwords match. If all checks out log in the user.
  :return: 200 if Success, else 400
  """
  values = request.values
  email = values['email']
  password = values['password']
  user_instance = User.get_by_email(email)
  login_status = False
  if user_instance:
    if user_instance.check_password(password):
      login_status = login_user(user_instance)
  if login_status:
    return jsonify(get_user_info())
  else:
    return 'invalid', 401


@app.route('/login-fb', methods=['POST'])
def login_fb():
  """
  POST route for logging in via facebook. First checks if user exists in the data base via the userID then checks via
  facebook if the accessToken and userID match each other. If all checks out log in the user.
  :return: 200 if Success, else 400
  """
  values = request.values
  access_token = values['accessToken']
  user_id = values['userID']
  user_instance = User.get_by_fb_id(user_id)
  login_status = False
  if user_instance:
    if fb_register.verify_token_and_id(user_id, access_token):
      login_status = login_user(user_instance)
  else:
    return jsonify({'statusMessage': 'no facebook account', 'path': 'facebook'}), 403
  if login_status:
    return jsonify(get_user_info())
  else:
    return 'invalid', 401


@app.route('/logout')
@login_required
def logout():
  logout_user()
  return 'ok'
