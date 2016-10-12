from flask import abort, Blueprint, jsonify, request
from flask.ext.login import current_user, login_required
from stogora_app.utils import nested_get
from json import loads
from stogora_app.models.photos import Photos

from stogora_app.models.listings import Listing

# check if csrf token is included and see if its matches the session


listings_bp = Blueprint('listing', __name__)

@listings_bp.route('/', methods=['POST'], strict_slashes=False)
@login_required
def submit_new_listing():
  """
  Get the necessary fields containing the information for a new listing
  :return: JSON with an attribute 'listing' whose value is the listing object's key value. It also contains user
  information
  """
  parsed_json = loads(request.data)
  values = nested_get(parsed_json, 'data.attributes')
  listing_attributes = {
    'title': values.get('title'),
    'price': values.get('price'),
    'stag_id': values.get('stag-id'),
    'user_id': current_user.id,
    'description': values.get('description'),
    'quantity': values.get('quantity'),
    'subtitle': values.get('subtitle'),
    'photo': values.get('photo'),
    'active': values.get('active')
  }

  listing = Listing(**listing_attributes)
  db_listing = Listing.create_new_listing(self=listing)

  if db_listing is not None:
    return jsonify({'data': listing.format_for_client()})
  else:
    abort()


@listings_bp.route('/', methods=['GET'], strict_slashes=False)
def get_all_listings():
  """
  Get listings created by the logged in user
  :return: Array of listings objects under the 'listings' attribute name
  """
  # user_listings = current_user.listings
  # listing_to_list_dict = [listing_instance.as_dict() for listing_instance in user_listings]
  # return jsonify({'listings': listing_to_list_dict})
  # return jsonify({'listings': all_listings})
  listings = Listing.get_all_listings()
  if listings:
    # return jsonify({'listings': [listing.format_for_client() for listing in listings]})
    return jsonify({
      'data': [listing.format_for_client(include_user=True) for listing in listings],
    })

  else:
    abort()


@listings_bp.route('/<int:listing_id>', methods=['GET'])
def listing_info(listing_id):
  """
  Get the listing information by the given id
  :param int listing_id: Id to query the listing row for
  :return: JSON of the key value pairs of the listing as well as the user information
  """
  listing = Listing.get_listing_by_id(listing_id)
  if listing is not None:
    return jsonify({'data': listing.format_for_client()})
  else:
    abort(404)

@listings_bp.route('/<int:listing_id>', methods=['DELETE'])
@login_required
def delete_listing(listing_id):
  """
  Get the listing information by the given id, check that the logged in user created it, and delete
  :param int listing_id: Delete the row with this id
  :return: JSON with message ok
  """
  listing = Listing.get_listing_by_id(listing_id)
  if listing.user_id == current_user.id:
    listing.delete()
    return jsonify({'message': 'ok'})
  else:
    abort(401)


@listings_bp.route('/<int:listing_id>', methods=['PATCH'])
@login_required
def update_by_listing_id(listing_id):
  """
  First check if the owner of the listing is the currently logged in user. Iterate through the list of updateable fields
  and check if they exist in the form of the request and that the keys are non null

  :param int listing_id: Listing to update attributes for
  :return:
  """
  listing_instance = Listing.get_listing_by_id(listing_id)
  if listing_instance.user_id == current_user.id:
    #values = request.json.get('listing')
    raw_json = loads(request.data)
    values = raw_json['data']['attributes']
    updateable_fields = ['title', 'price', 'description', 'quantity', 'subtitle', 'zip-loc', 'active']
    listing_attributes = {}
    for key in updateable_fields:
      if key in values and values[key]:
        listing_attributes[key] = values[key]
    listing_instance.update(listing_attributes)
    return jsonify({'data': listing_instance.format_for_client()})
  else:
    abort(401)

@listings_bp.route('/user/<int:user_id>', methods=['GET'])
def get_listings_by_user_id(user_id):
  user_listings = Listing.get_listing_by_user(user_id)
  if user_listings:
    return jsonify({'listings': [listing.format_for_client() for listing in user_listings]})
  else:
    abort()

@listings_bp.route('/photo/<int:listing_id>', methods=['POST'], strict_slashes=False)
@login_required
def post_listing_photo(listing_id):
  listing_instance = Listing.get_listing_by_id(listing_id)
  user_email = current_user.email
  if len(request.files) == 1:
    upload = request.files.values()[0]
    filename = str(listing_id)
  else:
    raise Exception("Bad Upload")
  return_url = Photos.upload_listing_photo(filename, upload, user_email)
  listing_instance.update({'photo': return_url})
  return jsonify({'data': listing_instance.format_for_client()})

