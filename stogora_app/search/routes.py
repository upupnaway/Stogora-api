from flask import Blueprint, jsonify, request

from stogora_app.models.listings import Listing

search_bp = Blueprint('search', __name__)


@search_bp.route('/', strict_slashes=False)
def get_search_results():
  key_words = request.args.get('keywords')
  if key_words:
    keys_words_split = key_words.split(' ')
    search_result = Listing.search_by_terms(keys_words_split)
    client_converted = [result.as_dict() for result in search_result]
    return jsonify({'meta': {'keywords': keys_words_split}, 'listings': client_converted})
  else:
    jsonify({'status': 'not ok'}), 500
