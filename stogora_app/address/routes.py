from flask import Blueprint, jsonify, request
from flask.ext.login import current_user, login_required

from stogora_app.models.address import Address
# TODO implement CSRF
from stogora_app.utils import csrf_verify

address_bp = Blueprint('address', __name__)


@address_bp.route('/', methods=['GET'], strict_slashes=False)
@login_required
def get_address_for_logged_in_user():
  """
  Using the logged in user's id, get all the addresses created by the user
  :return: JSON containing the list of addresses associated with the logged in user
  """
  addresses = current_user.addresses
  address_to_list_dict = [addr_instance.as_dict() for addr_instance in addresses]
  return jsonify({'addresses': address_to_list_dict})


@address_bp.route('/', methods=['POST'], strict_slashes=False)
@login_required
def create_new_address():
  """
  Create a new address with the values from the POST content
  :return: JSON of the new document created as a dictionary
  """
  # values = request.json.get('address')
  values = request.form
  address_attributes = {
    'name': values.get('name'),
    'street1': values.get('street1'),
    'street2': values.get('street2'),
    'city': values.get('city'),
    'state': values.get('state'),
    'zip_code': values.get('zip_code'),
    'country': values.get('country'),
    'phone': values.get('phone'),
    'user_id': current_user.id
  }
  address = Address(**address_attributes).add_to_db()
  return jsonify({'address': address.as_dict()})


@address_bp.route('/<int:address_id>', methods=['GET'])
@login_required
def get_by_address_id(address_id):
  """
  Get the document whose id equals the given id. For security and privacy reasons, make sure the person requesting the
  address created it
  :param int address_id: Row id to get the row of
  :return: JSON of the document contents
  """
  addr_instance = Address.get_by_id(address_id)
  if addr_instance.user_id == current_user.id:
    return jsonify({'address': addr_instance.as_dict()})
  else:
    return 'error', 401


@address_bp.route('/<int:address_id>', methods=['DELETE'])
@login_required
def delete_by_address_id(address_id):
  """
  Grab the row instance, make sure the user who is logged in owns the address, and delete it from the collection
  :param int address_id: Row id to delete
  :return: 200 if success or 401 if logged in user does not own document
  """
  addr_instance = Address.get_by_id(address_id)
  if addr_instance.user_id == current_user.id:
    addr_instance.delete()
    return 'ok', 200
  else:
    return 'error', 401


@address_bp.route('/<int:address_id>', methods=['PUT'])
@login_required
def update_by_address_id(address_id):
  """
  Grab the document associated with the id and then update the values from the POST contents.
  :param int address_id: Row ID to get and update
  :return: JSON of document
  """
  addr_instance = Address.get_by_id(address_id)
  if addr_instance.user_id == current_user.id:
    # values = request.json.get('address')
    values = request.form
    updateable_fields = ['name', 'street1', 'street2', 'city', 'state', 'zip_code', 'country', 'phone']
    address_attributes = {}
    for key in updateable_fields:
      if key in values and values[key]:
        address_attributes[key] = values[key]
    addr_instance.update(address_attributes)
    return jsonify({'address': addr_instance.as_dict()})
