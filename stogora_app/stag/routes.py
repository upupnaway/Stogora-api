from flask import abort, Blueprint, jsonify, request
from flask.ext.login import current_user, login_required

from stogora_app.models.stag import Stag
# TODO implement CSRF
from stogora_app.utils import csrf_verify

stags_bp = Blueprint('stag', __name__)

all_stags = [
  dict(id="2", name="ucberkeley", numUsers=355, numListings=500, stagPhoto=("http://hinshawsubdomain.dreamhosters.co"
                                                                            "m/wp-content/uploads/2014/03/cropped-ba"
                                                                            "nner1.jpg")),
  dict(id="3", name="photography", numUsers=100, numListings=20, stagPhoto=("http://imagesource.essaywriter.co.uk/st"
                                                                            "atic/photography-banner.jpg")),
  dict(id="4", name="s2000", numUsers=2000, numListings=3, stagPhoto=("http://ep.yimg.com/ty/cdn/yhst-1116174726211"
                                                                      "4/bumper-lip-spoiler-banner.JPG")),
  dict(id="1", name="everything", numUsers=2455, numListings=523)]


@stags_bp.route('/', methods=['GET'], strict_slashes=False)
def get_available_stags():
    # check to see which params were put in
    if request.args.get('slug') is not None:
      slug = '#{name}'.format(name=request.args.get('slug'))
      stags = Stag.get_stag_by_slug(slug)
      if stags is not None:
        return jsonify({'data': stags.format_for_client()})
      else:
        abort(404)

    else:
      stags = Stag.get_all_stags()
      return jsonify({'data': [stag.format_for_client() for stag in stags]})


@stags_bp.route('/active', methods=['GET'], strict_slashes=False)
def get_active_stags():
    stags = Stag.get_available_stags()
    return jsonify({'data': [stag.format_for_client() for stag in stags]})
