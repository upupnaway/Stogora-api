from datetime import datetime, timedelta
from random import choice, randint

from stogora_app.models import db
from stogora_app.models.users import User
from stogora_app.models.messages.conversation import Conversation
from stogora_app.models.messages.message import Message
from stogora_app.utils import timestamp


CONVERSATION = [
  'Bacon ipsum dolor amet filet mignon bacon tail boudin pig pork loin. Alcatra bresaola t-bone ham hock chicken tongue pork belly',
  'Bresaola capicola pancetta, kielbasa',
  'Landjaeger ribeye pork loin, venison frankfurter strip steak shank beef tri-tip picanha turducken cupim beef ribs tail. Cow bresaola jerky ground round bacon. Picanha doner pork chop chuck biltong. Swine cupim cow kielbasa biltong shankle, tri-tip bresaola beef sirloin drumstick. Turducken t-bone cow meatball.',
  'meatloaf pork chop t-bone',
  'ok'
]


def create_mock_conversations():
  conversation_pairs = {}
  available_users = db.session.query(User).all()

  iterations = 50
  while iterations > 0:
    iterations = iterations - 1

    # Select Two Users
    user_1 = choice(available_users)
    user_2 = choice(available_users)
    while user_1.id == user_2.id:
      user_2 = choice(available_users)

    users_array = [user_1, user_2]
    users_array.sort(key=lambda x: x.id)
    key = str(users_array[0].id) + str(users_array[1].id)

    if key in conversation_pairs:
      conversation = conversation_pairs[key]
    else:
      conversation = Conversation.create_conversation_for_users(users_array[0], users_array[1], None)
      conversation_pairs[key] = conversation

    msg = Message.create_with_user_conversation_and_content(choice(users_array), conversation, choice(CONVERSATION))
    msg.timestamp = timestamp(datetime.now() - timedelta(hours=randint(0, 24), minutes=randint(0, 60)))
    conversation.update_latest_message(msg)