from stogora_app.shipping import easypost_api


class Parcel(object):
  def __init__(self, weight, length, width, height):
    self.weight = weight
    self.length = length
    self.width = width
    self.height = height

  def easy_post_parcel(self):
    parcel_dict = self.__dict__
    return easypost_api.Parcel.create(parcel_dict)
