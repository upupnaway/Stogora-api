from stogora_app.models import db


class CommonFunctionsModelMixin():
  def as_dict(self):
    """
    Iterate through the column names and grab their value. Include the column name verbatim as the key
    :return: Dictionary whose keys are column names and their respective values
    """
    new_dict = {}
    for column in self.__table__.columns:
      new_dict[column.name] = getattr(self, column.name)
    self.post_as_dict_hook(new_dict)
    return new_dict

  def post_as_dict_hook(self, new_dict):
    """
    Hook created to be overwritten for special cases
    :param dict new_dict: Dict object to be returned
    :return: The dict from the parameter
    """
    return new_dict

  def update(self, attributes, delay_commit=False):
    """
    Pragmatic update function
    :param dict attributes: Dict of attributes to be updated
    :param boolean delay_commit: Indicates whether to delay the commit or not (for batch updates)
    :return: The instance object
    """
    for key, value in attributes.iteritems():
      setattr(self, key, value)
    if not delay_commit:
      db.session.commit()
    return self

  def delete(self, delay_commit=False):
    """
    Call the session delete function passing the model instance
    :param boolean delay_commit: Indicated whether to delay the db commit or not (for batch deletes)
    :return:
    """
    db.session.delete(self)
    if not delay_commit:
      db.session.commit()

  def add_to_db(self):
    """
    #TODO Need to wrap around try catch
    :return:
    """
    db.session.add(self)
    db.session.commit()
    return self

  @classmethod
  def get_by_id(cls, row_id):
    """
    Query for row with the given id
    :param int row_id: ID of row to get
    :return: Row instance or None
    """
    return db.session.query(cls).filter(cls.id == row_id).first()
