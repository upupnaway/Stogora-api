from flask import abort, Blueprint, jsonify, request
from flask.ext.login import current_user, login_required

from stogora_app.models.users import User

users_bp = Blueprint('user', __name__)


@users_bp.route('/', methods=['GET'], strict_slashes=False)
def get_all_users():
  users = User.get_all_users()
  if users:
    return jsonify({'data': [user.as_dict_safe_client() for user in users]})
  else:
    abort()


@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
  user = User.get_by_id(user_id)
  if user:
    return jsonify({'data': user.as_dict_safe_client()})
  else:
    abort()
