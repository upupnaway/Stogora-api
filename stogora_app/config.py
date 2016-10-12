import os
from datetime import timedelta

environment = os.environ.get('SERVER_ENVIRONMENT')

if environment == 'PRODUCTION':
  DEBUG = False
  FB_APP_ID = 'xxxxxxxx'
  FB_APP_SECRET = 'xxxxxxx'
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
else:
  DEBUG = True
  FB_APP_ID = 'xxxxxxx'
  FB_APP_SECRET = 'xxxxxxxx'
  SQLALCHEMY_DATABASE_URI = 'xxxxxxxx'
  # SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/stogora_dev'

MONGO_HOST = 'xxxxxxxx'  # 'localhost:27017
MONGO_DB_NAME = 'xxxxx'
REMEMBER_COOKIE_DURATION = timedelta(days=7)
EASY_POST_API_KEY = 'xxxxxxxx'
AWS_ACCESS_KEY = 'xxxxxxxxx'
AWS_SECRET_KEY = 'xxxxxxxxxx'
