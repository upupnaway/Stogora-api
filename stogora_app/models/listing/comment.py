from datetime import datetime

from stogora_app.models import db
from stogora_app.models.common_functions_model_mixin import CommonFunctionsModelMixin
from stogora_app.utils import timestamp


class ListingComment(db.Model, CommonFunctionsModelMixin):
  __tablename__ = 'listing_comments'
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id', use_alter=True, name='fk_comment_user_id'))
  listing_id = db.Column(db.Integer, db.ForeignKey('listings.id', use_alter=True, name='fk_comment_listing_id'))
  message = db.Column(db.Text)
  timestamp = db.Column(db.Integer)

  user = db.relationship('User', backref=db.backref('listing_comments', lazy='dynamic'), lazy='joined', foreign_keys=[user_id])

  def format_for_client(self):
    return {
      'type': 'listing-comment',
      'id': self.id,
      'attributes': {
        'message': self.message,
        'author': self.user.full_name,
        'author-id': self.user_id,
        'timestamp': self.timestamp
      },
      'relationships': {
        'listing': {
          'data': {
            'id': self.listing_id,
            'type': 'listing'
          }
        },
        'user': {
          'data': self.user.as_dict_safe_client()
        }
      }
    }

  @classmethod
  def get_comments_for_listing(cls, listing_id):
    """
    Query database for rows with the matching listing id
    :param int listing_id: Listing id to query for
    :return: Rows with the matching listing id
    """
    return db.session.query(cls).filter(cls.listing_id == listing_id).all()

  @classmethod
  def create_new_comment(cls, user_id, message, listing_id):
    new_inst = cls(user_id=user_id, message=message, listing_id=listing_id, timestamp=timestamp(datetime.now()))
    try:
      db.session.add(new_inst)
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      raise e
    return new_inst