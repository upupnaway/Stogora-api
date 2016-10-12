from flask import Blueprint, jsonify, request
from flask.ext.login import current_user, login_required
from json import loads

from stogora_app.models.following import Following
from stogora_app.models.users import User
from stogora_app.utils import nested_get

following_bp = Blueprint('following', __name__)


@following_bp.route('/', methods=['GET'])
@login_required
def get_followings():
  """
  Get the all the followings for the logged in user
  :return: JSON of the list of followed users
  """
  followings = Following.get_followings_for_user_id(current_user.id)
  return jsonify({'data': [following.format_for_client() for following in followings]})


@following_bp.route('/user/<int:user_following_id>', methods=['GET'])
@login_required
def get_following_status_for_user(user_following_id):
  """
  Check if the logged in user is following the user with the given id.

  :param int user_following_id: Id of the user to to check that is being followed
  :return: 404 if not found else the following instance
  """
  following = Following.get_following_for_follower_and_following(current_user.id, user_following_id)
  if following:
    response_data = following.format_for_client()
  else:
    return jsonify({'data': {}}), 404
  return jsonify({'data': response_data})


@following_bp.route('/<int:following_row_id>', methods=['DELETE'])
@login_required
def remove_following(following_row_id):
  """
  Call the model function to delete the following with the matching row if
  :param int following_row_id: Row id to delete
  :return: JSON of the row that was deleted for the client
  """
  following = Following.get_by_id(following_row_id)
  if following:
    following.delete()
  return jsonify({'data': following.format_for_client()})


@following_bp.route('/', methods=['POST'], strict_slashes=False)
@login_required
def follow_a_user():
  """
  First check that the given user to follow does not match the logged in user, then proceed to check that the given user
  id exists. If all are valid, create a new following instance with the logged in user as the follower and the if in the
  post body as the followed

  :return: JSON of the following instance just created else 500 if there was an error
  """
  parsed_json = loads(request.data)
  following_id = nested_get(parsed_json, 'data.attributes.following-id')
  if following_id and int(following_id) != current_user.id:
    # Make sure the user exists
    user_to_be_followed = User.get_by_id(int(following_id))
    if user_to_be_followed:
      following_instance = Following.create_follower_for_users(current_user, user_to_be_followed)
      return jsonify({'data': following_instance.format_for_client()})
  return 'not ok', 500