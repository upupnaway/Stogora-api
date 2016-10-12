from stogora_app.models import client, db
from stogora_app.models.common_functions_model_mixin import CommonFunctionsModelMixin

listings_collection = client.listings


class Listing(db.Model, CommonFunctionsModelMixin):
  __tablename__ = 'listings'
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(120), index=True)
  subtitle = db.Column(db.Text)
  description = db.Column(db.Text)
  price = db.Column(db.Integer)
  quantity = db.Column(db.Integer)
  photo = db.Column(db.Text)
  active = db.Column(db.Boolean, default=False)
  sold = db.Column(db.Boolean, default=False)
  stag_id = db.Column(db.Integer, db.ForeignKey('stags.id'))
  stag = db.relationship('Stag')

  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  user = db.relationship('User', backref=db.backref('listings', lazy='dynamic'))

  def format_for_client(self, include_user=False):
    relationship_portion = {
      'user': {
        'data': self.user.as_dict_safe_client()
      }
    }
    serialized = {
      'type': 'listing',
      'id': self.id,
      'attributes': {
        'title': self.title,
        'subtitle': self.subtitle,
        'description': self.description,
        'price': self.price,
        'quantity': self.quantity,
        'photo': self.photo,
        'stag-id': self.stag_id,
        'user-id': self.user_id,
        'active': self.active,
        'sold': self.sold
      },
      'relationships': {'user': [self.user.as_dict_safe_client()]}
    }
    if include_user:
      user_list = {'id': self.user.id, 'type': 'user'}
      relationship_portion = {
        'user': {
          'data': user_list
        }
      }
      serialized['relationships'] = relationship_portion

    return serialized

  def post_as_dict_hook(self, new_dict):
    new_dict['user'] = self.user.as_dict_safe_client()

  @classmethod
  def get_all_listings(cls):
    return db.session.query(cls).filter(cls.active == True).all()

  @classmethod
  def get_listing_by_id(cls, row_id):
    """
    Query database table for row with the given id
    :param int row_id: Row id to query for
    :return: The sqlalchemy row instance for the row or None
    """
    return db.session.query(cls).filter(cls.id == row_id).first()

  @classmethod
  def get_listing_by_user(cls, user_id):
    """
    Query database table for rows with the given user id
    :param int user_id: User id to query for
    :return: List of sqlalchemy row instances with the user id or empty list
    """
    return db.session.query(cls).filter(cls.user_id == user_id).all()

  @classmethod
  def create_new_listing(cls, self):
    new_inst = self
    try:
      db.session.add(new_inst)
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      raise e
    return new_inst

  @staticmethod
  def search_by_terms(key_words):
    space_seperated = ' '.join(key_words)
    search_results = client.command('text', 'listings', search=space_seperated)
    doc_matches = (Listing._create_instance_from_mongo_document(res['obj']) for res in search_results['results'])
    return doc_matches
