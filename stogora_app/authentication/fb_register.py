from flask import current_app

from collections import namedtuple
from requests import codes, request

FBUserInfo = namedtuple('FBUserInfo', ['user_info', 'photo_url', 'friends'])
FB_GRAPH_HOSTNAME = 'https://graph.facebook.com'
SEVER_ACCESS_TOKEN = '/oauth/access_token?client_id={app_id}&client_secret={app_secret}&grant_type=client_credentials'
TOKEN_VERIFY = '/debug_token?input_token={token}&access_token={server_access_token}'
USER_INFO = 'https://graph.facebook.com/v2.3/me?access_token={token}'
USER_PHOTO = 'https://graph.facebook.com/v2.3/me/picture?access_token={token}&width=1000&height=1000'
FRIEND_LIST = 'https://graph.facebook.com/v2.3/me/friends?access_token={token}'


class FBServerException(Exception):
  pass


class FBVerificationException(Exception):
  pass


def get_access_token():
  """
  Format the url to get the server access token and make a request via HTTPS. The response from the fb api is assumed to
  be in the format of "access_token=SOMETOKEN" so the token is extracted out.
  :return: The FB access token for the server
  """
  formatted_path = SEVER_ACCESS_TOKEN.format(app_id=current_app.config.get('FB_APP_ID'),
                                             app_secret=current_app.config.get('FB_APP_SECRET'))
  server_access_token_request = request('GET', FB_GRAPH_HOSTNAME + formatted_path)
  access_token_data = server_access_token_request.text
  return access_token_data.replace('access_token=', '')


def verify_token_and_id(user_id, token):
  """
  Perform a GET request to the FB server to check what user id is associated with the given token. Compare that response
  from the fb server against the given user id
  :param str user_id: Facebook user id
  :param str token: Facebook access token to check if the user id binded to it matches
  :return: True if the token is for the given user_id, False otherwise
  """
  server_access_token = get_access_token()
  verify_url = FB_GRAPH_HOSTNAME + TOKEN_VERIFY.format(token=token, server_access_token=server_access_token)
  verify_request = request('GET', verify_url)
  if verify_request.status_code == codes.ok:
    verification_results_data = verify_request.json()['data']
    return verification_results_data.get('user_id') == user_id
  elif 400 >= verify_request.status_code < 500:
    raise FBVerificationException(verify_request.json()['error']['message'])
  elif verify_request >= 500:
    raise FBServerException('FB Server Error')
  else:
    raise Exception('Unknown Error in Token Verification')


def get_fb_user_info(access_token):
  """
  For the given access code get the user info from the graph api from facebook. The photo is 1000x1000 and the friends
  list only returns those who also have an account with the app
  :param str access_token: Acess token to use
  :return: Named Tuple with user_info, photo_url, and friends_list
  """
  user_info = request('GET', USER_INFO.format(token=access_token)).json()
  photo_url = request('GET', USER_PHOTO.format(token=access_token)).url
  # {u'data': [], u'summary': {u'total_count': 1149}}
  friends_list = request('GET', FRIEND_LIST.format(token=access_token)).json()
  return FBUserInfo(user_info, photo_url, friends_list['data'])
