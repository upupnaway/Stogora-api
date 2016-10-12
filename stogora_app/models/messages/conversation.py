from sqlalchemy import and_, or_

from stogora_app.models import db
from stogora_app.models.messages.message import Message


class Conversation(db.Model):
  __tablename__ = 'conversations'
  id = db.Column(db.Integer, primary_key=True)
  user_id_1 = db.Column(db.Integer, db.ForeignKey('users.id', use_alter=True, name='fk_convo_user1_id'), index=True)
  user_id_2 = db.Column(db.Integer, db.ForeignKey('users.id', use_alter=True, name='fk_convo_user2_id'), index=True)
  latest_message_id = db.Column(db.Integer, db.ForeignKey('messages.id'))

  user_1 = db.relationship('User', lazy='joined', foreign_keys=[user_id_1])
  user_2 = db.relationship('User', lazy='joined', foreign_keys=[user_id_2])
  latest_message = db.relationship('Message', lazy='joined', foreign_keys=[latest_message_id])

  @property
  def last_message_timestamp(self):
    return self.latest_message.timestamp

  def user_is_in_conversation(self, user):
    user_id_to_check = user.id
    return user_id_to_check == self.user_id_1 or user_id_to_check == self.user_id_2

  def format_for_client(self, user_not_to_include, include_messages=False):
    user_id_to_not_include = user_not_to_include.id
    user_to_send_to_client = self.user_1
    if self.user_id_2 != user_id_to_not_include:
      user_to_send_to_client = self.user_2


    serialized = {
      'type': 'conversations',
      'id': self.id,
      'attributes': {
        'partner-id': user_to_send_to_client.id,
        'partner-name': user_to_send_to_client.full_name,
        'last-messaged': self.latest_message.timestamp,
        'last-message-blurb': self.latest_message.content
      }
    }
    if include_messages:
      messages_list = [{'id': msg.id, 'type': 'message'} for msg in self.messages]
      relationship_portion = {
        'messages': {
          'data': messages_list
        }
      }
      serialized['relationships'] = relationship_portion

    return serialized

  def update_latest_message(self, message):
    """
    Set the latest_message_id to given message id and save it to the database

    :param :Message message: Message instance
    :return: Return Conversation instance
    """
    self.latest_message_id = message.id
    try:
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      raise e
    return self

  def get_messages(self, limit):
    query = self.messages.order_by(Message.timestamp)
    if limit:
      query = query.limit(limit)
    return query.all()

  @classmethod
  def find_conversation_for_users(cls, user_id_1, user_id_2):
    """
    Query for the row with the matching users

    :param int user_id_1: User id of one end of the conversation
    :param int user_id_2: User id of the other end of conversation
    :return: Conversation row instance if it exists otherwise None
    """
    row = db.session.query(cls).filter(or_(and_(cls.user_id_1 == user_id_1, cls.user_id_2 == user_id_2),
                                           and_(cls.user_id_2 == user_id_1, cls.user_id_1 == user_id_2))).first()
    return row

  @classmethod
  def find_conversations_for_id(cls, conversation_id):
    row = db.session.query(cls).filter(cls.id == conversation_id).first()
    return row

  @classmethod
  def find_conversations_for_user(cls, user_id):
    rows = db.session.query(cls).filter(or_(cls.user_id_1 == user_id, cls.user_id_2 == user_id)).all()
    return rows

  @classmethod
  def create_conversation_for_users(cls, user_1, user_2, latest_message_id):
    new_insta = cls(user_id_1=user_1.id, user_id_2=user_2.id, latest_message_id=latest_message_id)
    try:
      db.session.add(new_insta)
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      raise e
    return new_insta
