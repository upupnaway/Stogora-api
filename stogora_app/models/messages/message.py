from datetime import datetime

from stogora_app.models import db
from stogora_app.utils import timestamp

class Message(db.Model):
  __tablename__ = 'messages'
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id', use_alter=True, name='fk_msg_user_id'))
  conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id', use_alter=True, name='fk_convo_sg_id'))
  timestamp = db.Column(db.Integer)
  content = db.Column(db.Text)

  conversation = db.relationship('Conversation', backref=db.backref('messages', lazy='dynamic'), lazy='joined', foreign_keys=[conversation_id])
  user = db.relationship('User', backref=db.backref('messages', lazy='dynamic'), lazy='joined', foreign_keys=[user_id])

  def format_for_client(self):
    return {
      'type': 'messages',
      'id': self.id,
      'attributes': {
        'message': self.content,
        'sender': self.user.full_name,
        'sender-id': self.user_id,
        'timestamp': self.timestamp
      },
      'relationships': {
        'conversation': {
          'data': {
            'id': self.conversation_id,
            'type': 'conversation'
          }
        }
      }
    }

  @classmethod
  def create_with_user_conversation_and_content(cls, user, conversation, content):
    """
    Create new instance with given params and save to database
    :param :User user: User who wrote message
    :param :Conversation conversation: Conversation to associate message with
    :param str content: String of the message content
    :return:
    """
    current_ts = timestamp(datetime.now())
    new_inst = cls(user_id=user.id, conversation_id=conversation.id, timestamp=current_ts, content=content)
    try:
      db.session.add(new_inst)
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      raise e
    return new_inst