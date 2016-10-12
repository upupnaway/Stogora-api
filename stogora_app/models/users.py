from pbkdf2 import _makesalt, crypt

from flask.ext.login import UserMixin
from stogora_app.models import db
from stogora_app.models.common_functions_model_mixin import CommonFunctionsModelMixin


class User(db.Model, UserMixin, CommonFunctionsModelMixin):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  user_name = db.Column(db.String(80))
  first_name = db.Column(db.String(80))
  last_name = db.Column(db.String(80))
  email = db.Column(db.Text)
  fb_user_id = db.Column(db.Text)
  profile_photo = db.Column(db.Text)
  rating = db.Column(db.Integer)
  points = db.Column(db.Integer)
  salt = db.Column(db.Text)
  encrypted_password = db.Column(db.Text)

  def __init__(self, first_name=None, last_name=None, email=None, password=None, fb_user_id=None, profile_photo=None,
               points=0, rating=None, user_name=None):
    self.id = None
    self.user_name = user_name
    self.first_name = first_name
    self.last_name = last_name
    self.email = email
    self.fb_user_id = fb_user_id
    self.profile_photo = profile_photo
    self.points = points
    self.rating = rating
    if password:
      self.salt = _makesalt()
      self.encrypted_password = crypt(password, self.salt)
    else:
      self.salt = None
      self.encrypted_password = None

  @property
  def full_name(self):
    return self.first_name + ' ' + self.last_name

  def check_password(self, password):
    """
    Encrypts the given password with the salt and then checks if it matches the stored encrypted password
    :param str password: Password to cross check with encrypted
    :return: True if a match else False
    """
    return crypt(password, self.salt) == self.encrypted_password

  def as_dict_safe_client(self):
    """
    Return information that simply identifies user without credentials related information
    :return: Dictionary whose keys are related to user information
    """
    return {
      'type': 'user',
      'id': self.id,
      'attributes': {
        'first-name': self.first_name,
        'last-name': self.last_name,
        'user-name': self.user_name,
        'profile-photo': self.profile_photo,
        'points': self.points,
        'rating': self.rating
      }
    }

  def as_sub_attr_client(self):
    return {
      'id': self.id,
      'first-name': self.first_name,
      'last-name': self.last_name,
      'user-name': self.user_name,
      'profile-photo': self.profile_photo,
      'points': self.points,
      'rating': self.rating
    }

  def save(self):
    db.session.add(self)
    db.session.commit()
    return self

  @classmethod
  def does_exist(cls, email):
    """
    Queries the collection for any documents with the given email. Return True if there is one already else False.
    :param str email: Email address to check if it already exists
    :return: True if a document already uses the email
    """
    query_result = db.session.query(cls).filter(cls.email == email).first()
    return query_result is not None

  @classmethod
  def does_exist_fb(cls, fb_id):
    """
    Queries the collection for any documents with the given facebook user id. Return True if there is one already else
    False.
    :param str fb_id: String of the facebook user id
    :return: True if a document already uses the facebook id
    """
    query_result = db.session.query(cls).filter(cls.fb_user_id == fb_id).first()
    return query_result is not None

  @classmethod
  def get_all_users(cls):
    return db.session.query(cls).all()

  @classmethod
  def get_by_email(cls, email):
    return db.session.query(cls).filter(cls.email == email).first()

  @classmethod
  def get_by_fb_id(cls, fb_id):
    return db.session.query(cls).filter(cls.fb_user_id == fb_id).first()
