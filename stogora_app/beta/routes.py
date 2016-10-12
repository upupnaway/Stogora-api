from flask import Blueprint, jsonify, request
from stogora_app.models.beta import Beta

betas = Blueprint('beta', __name__)


@betas.route('/', methods=['POST'], strict_slashes=False)
def submit_user_email():
  values = request.json.get('beta')
  user_attributes = {'email': values['email']}
  beta = Beta(**user_attributes).save()
  return jsonify({'status': 'email saved'})
