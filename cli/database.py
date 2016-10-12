#!venv/bin/python
from flask.ext.script import Manager, prompt_bool, Server, Shell

from stogora_app import app, db
from stogora_app.models.listings import Listing
from stogora_app.models.users import User
from stogora_app.models.stag import Stag

from cli import data_generator
from cli.data_generator.messages import create_mock_conversations

manager = Manager(usage="Perform database operations")


@manager.command
def setup_db():
  'Creates tables'
  db.create_all()

@manager.command
def drop_all():
  'Drops address, users, categories, and listings'
  check_for_localhost()
  if prompt_bool('Are you sure you want to clear all the documents?'):
    db.drop_all()

@manager.command
def reset():
  'Drops address, users, categories, and listings. Creates text index on listings. Populates listings and users'
  if prompt_bool('Are you sure you want to reset?'):
    db.drop_all()
    db.create_all()
    populate()


@manager.command
def populate():
  'Populate database with default data'
  check_for_localhost()
  users_data = data_generator.generate_users()

  user_db_model_instances = []
  for user_data in users_data:
    user_model_inst = User(**user_data)
    user_db_model_instances.append(user_model_inst.add_to_db())

  stags_data = data_generator.generate_stags()
  stag_instances = []
  for stag_data in stags_data:
    stag_model_inst = Stag(**stag_data)
    stag_instances.append(stag_model_inst.add_to_db())

  listings_data = data_generator.generate_listings(user_db_model_instances, stag_instances)
  for listing_data in listings_data:
    listing_model_inst = Listing(**listing_data)
    listing_model_inst.add_to_db()

  create_mock_conversations()

def check_for_localhost():
  localhosts = ['0.0.0.0', 'localhost', '127.0.0.1']
  is_localhost = False

  """
  for localhost in localhosts:
    if localhost in MONGO_HOST:
      is_localhost = True
      break

  if is_localhost:
    return True
  else:
    print('Make sure your configs (MONGO_HOST) is set to localhost')
    sys.exit(1)
  """
  return True