from json import loads

from flask import Blueprint, jsonify, request
from flask.ext.login import current_user, login_required

from stogora_app.models.messages.conversation import Conversation
from stogora_app.models.messages.message import Message

message_thread_bp = Blueprint('message_thread', __name__)


@message_thread_bp.route('/conversations/<int:conversation_id>', strict_slashes=False)
@login_required
def get_conversation_with_user(conversation_id):
  limit = request.args.get('limit', 25)
  date_max = request.args.get('datemax')
  conversation = Conversation.find_conversations_for_id(conversation_id)
  messages = conversation.get_messages(limit)
  formatted_for_client = [msg.format_for_client() for msg in messages]

  return jsonify({
    'data': conversation.format_for_client(current_user, include_messages=True),
    'included': formatted_for_client
  })


@message_thread_bp.route('/conversations', strict_slashes=False)
@login_required
def message_threads():
  if request.args.get('id'):
    return get_conversation_with_user(request.args.get('id'))
  conversations = Conversation.find_conversations_for_user(current_user.id)
  formatted_for_client = [conversation.format_for_client(current_user) for conversation in conversations]
  return jsonify({'data': formatted_for_client})


@message_thread_bp.route('/messages', methods=['POST'])
@login_required
def create_new_message():
  """
  Grab the message, find the conversation, check that the logged in user is part of the conversation, then finally
  create a new message

  :return:
  """
  parsed_json = loads(request.data)
  msg_content = parsed_json['data']['attributes']['message']
  conversation_id = parsed_json['data']['relationships']['conversation']['data']['id']
  conversation = Conversation.find_conversations_for_id(int(conversation_id))
  fail_status = 500
  try:
    if conversation.user_is_in_conversation(current_user):
      msg = Message.create_with_user_conversation_and_content(current_user, conversation, msg_content)
      conversation.update_latest_message(msg)
      return jsonify({'data': msg.format_for_client()})
    else:
      fail_status = 401
  except Exception as e:
    pass
  return jsonify({'status': 'not ok'}), fail_status