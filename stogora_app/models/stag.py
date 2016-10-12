from sqlalchemy.orm import relationship

from stogora_app.models import client, db
from stogora_app.models.common_functions_model_mixin import CommonFunctionsModelMixin

listings_collection = client.listings


class Stag(db.Model, CommonFunctionsModelMixin):
  __tablename__ = 'stags'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(120), index=True)
  # url component e.g. r/<slug>
  slug = db.Column(db.String(120), index=True, unique=True)
  stag_photo = db.Column(db.Text)
  listings = relationship('Listing', backref=db.backref('stags', lazy='subquery'))

  def format_for_client(self):
    return {
      'type': 'stag',
      'id': self.id,
      'attributes': {
        'name': self.name,
        'slug': self.slug,
        'stag-photo': self.stag_photo,
      }
    }

  @classmethod
  def get_stag_by_slug(cls, slug):
    """
    Query database table for row with the given slug
    :param str slug: slug to query for
    :return: The sqlalchemy row instance for the row with matching slug or None
    """
    return db.session.query(cls).filter(cls.slug == slug).first()

  @classmethod
  def get_all_stags(cls):
    """
    Get all the stags
    :return: All the stags in the table
    """
    return db.session.query(cls).all()

  @classmethod
  def get_available_stags(cls):
    """
    Get all stags that user can post in
    :return: All stags minus #everything in the table
    """
    return db.session.query(cls).filter(cls.slug != '#everything')
