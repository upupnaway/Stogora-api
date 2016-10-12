from stogora_app.shipping import easypost_api


class Shipment(object):
  def __init__(self, to_address, from_address, parcel):
    self.to_address = to_address
    self.from_address = from_address
    self.parcel = parcel
    self.easy_post_shipment_response = self._easy_post_shipment()

  def _easy_post_shipment(self):
    return easypost_api.Shipment.create(to_address=self.to_address.__dict__,
                                        from_address=self.from_address.__dict__,
                                        parcel=self.parcel.__dict__)

  @property
  def rates(self):
    return dict([(rate['service'], rate) for rate in self.easy_post_shipment_response['rates']])
