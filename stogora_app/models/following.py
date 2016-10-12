from datetime import datetime

from stogora_app.models import db
from stogora_app.models.common_functions_model_mixin import CommonFunctionsModelMixin
from stogora_app.utils import timestamp


class Following(db.Model, CommonFunctionsModelMixin):
  __tablename__ = 'follower'
  id = db.Column(db.Integer, primary_key=True)
  follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
  following_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
  created_at = db.Column(db.Integer)

  follower = db.relationship('User', lazy='joined', foreign_keys=[follower_id])
  following = db.relationship('User', lazy='joined', foreign_keys=[following_id])
  __table_args__ = (db.UniqueConstraint('follower_id', 'following_id'), )

  def format_for_client(self):
    return {
      'type': 'following',
      'id': self.id,
      'attributes': {
        'created-at': self.created_at,
        'following-id': self.following_id,
      },
      'relationships': {'user': [self.following.as_dict_safe_client()]}
    }

  def post_as_dict_hook(self, new_dict):
    new_dict['user'] = self.user.as_dict_safe_client()

  @classmethod
  def get_followings_for_user_id(cls, user_id):
    return db.session.query(cls).filter(cls.follower_id == user_id).all()

  @classmethod
  def get_following_for_follower_and_following(cls, follower_id, following_id):
    return db.session.query(cls).filter(cls.follower_id == follower_id).filter(cls.following_id == following_id).first()

  @classmethod
  def create_follower_for_users(cls, follower, following):
    """
    Create a following instance and save it to the db

    :param :User follower: User that is following
    :param :User following: User to be followed
    :return: New instance that was created
    """
    ts_now = timestamp(datetime.now())
    new_insta = cls(follower_id=follower.id, following_id=following.id, created_at=ts_now)
    try:
      db.session.add(new_insta)
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      raise e
    return new_insta
