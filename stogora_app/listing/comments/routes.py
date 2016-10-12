from flask import Blueprint, jsonify, request
from flask.ext.login import current_user, login_required
from json import loads

from stogora_app.models.listings import Listing
from stogora_app.models.listing.comment import ListingComment


listing_comment_bp = Blueprint('listing_comment', __name__)


@listing_comment_bp.route('/', methods=['POST'], strict_slashes=False)
@login_required
def create_new_comment():
  """
  Extract message and listing id from json data. Check if the listing exists for the given id, then create a
  new listing comment
  :return: JSON of the newly created comment
  """
  parsed_json = loads(request.data)
  msg_content = parsed_json['data']['attributes']['message']
  listing_id = parsed_json['data']['relationships']['listing']['data']['id']
  listing = Listing.get_by_id(int(listing_id))
  fail_status = 500
  try:
    if listing:
      listing_msg = ListingComment.create_new_comment(current_user.id, msg_content, listing.id)
      return jsonify({'data': listing_msg.format_for_client()})
    else:
      fail_status = 401
  except Exception as e:
    pass
  return jsonify({'status': 'not ok'}), fail_status


@listing_comment_bp.route('/listing/<int:listing_id>')
def get_comments_for_listing(listing_id):
  """
  Get all the comments for the given id
  :param int listing_id: Listing id to get comments for
  :return: Comments for listing
  """
  comments = ListingComment.get_comments_for_listing(listing_id)
  return jsonify({'data': [comment.format_for_client() for comment in comments]})