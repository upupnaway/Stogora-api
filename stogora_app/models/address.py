from stogora_app.models import db
from stogora_app.models.common_functions_model_mixin import CommonFunctionsModelMixin


class Address(db.Model, CommonFunctionsModelMixin):
  __tablename__ = 'addresses'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80))
  street1 = db.Column(db.Text)
  street2 = db.Column(db.Text)
  city = db.Column(db.Text)
  state = db.Column(db.Text)
  zip_code = db.Column(db.Text)
  country = db.Column(db.Text)
  phone = db.Column(db.Text)

  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  user = db.relationship('User', backref=db.backref('addresses', lazy='dynamic'))

  def __repr__(self):
    return '<Address %d>' % self.id

  @classmethod
  def get_by_user_id(cls, user_id):
    """
    Query database table for rows with the given use id
    :param int user_id: Row id from the users table
    :return: List of row instances or empty list
    """
    addresses = db.session.query(cls).filter(cls.user_id == user_id)
    return addresses.all()

  @classmethod
  def get_by_id(cls, row_id):
    """
    Query database table for specific row with id
    :param int row_id: Row to query for
    :return: The row instance with the matching id or none
    """
    return db.session.query(cls).filter(cls.id == row_id).first()
