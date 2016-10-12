from pymongo import MongoClient
from boto import connect_s3

from stogora_app import db as app_db
from stogora_app.config import MONGO_DB_NAME, MONGO_HOST, AWS_ACCESS_KEY, AWS_SECRET_KEY

client = MongoClient(MONGO_HOST)[MONGO_DB_NAME]
conn = connect_s3(AWS_ACCESS_KEY, AWS_SECRET_KEY)

# Centralize the db connection
db = app_db
