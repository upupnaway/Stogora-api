from __future__ import division
from flask import abort, request, session
from functools import wraps
from datetime import datetime


def csrf_verify(func):
  """
  Grab the csrf attribute from the post values and check it with the session's csrf token
  :param func: Function to wrap the csrf check
  :return: Function where the csrf check occurs before hand
  """

  @wraps(func)
  def decorated_view(*args, **kwargs):
    values = request.values
    if values.get('csrf') == session['_csrf']:
      return func(*args, **kwargs)
    return abort(401)

  return decorated_view


def timestamp(dt, epoch=datetime(1970, 1, 1)):
  """
  Convert datetime object into timestamp in seconds from epoch
  :param datetime dt: Datetime object to convert into seconds
  :param epoch:
  :return:
  """
  td = dt - epoch
  return int((td.microseconds + (td.seconds + td.days * 86400) * 10 ** 6) / 10 ** 6)


def nested_get(dictionary, path):
  """
  Helper function to get attributes from multilayer dictionary. Returns None if the path doesn't exist

  :param dict dictionary: Dictionary to get attributes from
  :param str path: String dot separated for example: 'data.attributes.stuff'
  :return:
  """
  steps = path.split('.')
  current_value = dictionary
  for step in steps:
    if step in current_value:
      current_value = current_value[step]
    else:
      return None
  return current_value