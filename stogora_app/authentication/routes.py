from flask import Blueprint, jsonify, request, session
from flask.ext.login import current_user, login_user

from stogora_app.authentication import fb_register
from stogora_app.models.users import User

authentication = Blueprint('authentication', __name__)


@authentication.route('/register-fb', methods=['POST'])
def register_new_user_fb():
  """
  Verify that the access token and user id are actually correct. If so, get the user information from the facebook apis
  :return:
  """
  values = request.values
  access_token = values['accessToken']
  user_id = values['userID']
  if fb_register.verify_token_and_id(user_id, access_token):
    data = fb_register.get_fb_user_info(access_token)
    user_info = data.user_info
    if not User.does_exist_fb(user_id):
      if not User.does_exist(user_info['email']):
        user = User(user_info['first_name'], user_info['last_name'], user_info['email'], None, user_id, None)
        user.save()
        login_user(User.get_by_fb_id(user_id))
        return jsonify({'userInfo': get_user_info(), 'status': 'authenticated'})
      else:
        return jsonify({'statusMessage': 'email duplication', 'path': 'facebook'}), 403
    else:
      return jsonify({'statusMessage': 'facebook duplication', 'path': 'facebook'}), 403

  return 'Invalid', 500


@authentication.route('/register', methods=['POST'])
def register_new_user():
  """
  Extract the email, first name, last name, and passwords fields from the POST data and create a new user if the it has
  not already been create.
  :return:
  """
  values = request.values
  email = values['email']
  first_name = values['firstName']
  last_name = values['lastName']
  password = values['password']
  if not User.does_exist(email):
    user = User(first_name, last_name, email, password, None, None)
    user.save()
    login_user(User.get_by_email(email))
    return jsonify(get_user_info())
  else:
    return jsonify({'statusMessage': 'email duplication', 'path': 'traditional'}), 403
  return 'Invalid', 500


@authentication.route('/authentication-info')
def authentication_info():
  if current_user.is_authenticated():
    return jsonify(get_user_info())
  else:
    return jsonify({}), 403


def get_user_info():
  return {
    'csrfToken': session['_csrf'],
    'id': current_user.id,
    'firstName': current_user.first_name,
    'lastName': current_user.last_name,
    'email': current_user.email
  }
