from stogora_app.shipping import easypost_api


class AddressEasyPostMixin(object):
  def verified_address(self):
    address_dict = self.__dict__
    try:
      verified_address = easypost_api.Address.create(**address_dict).verify()
    except easypost_api.Error as e:
      raise e
    return verified_address

  def easy_post_address(self):
    address_dict = self.__dict__
    return easypost_api.Address.create(**address_dict)
