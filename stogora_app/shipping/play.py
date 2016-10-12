from stogora_app.shipping.address import Address
from stogora_app.shipping.parcel import Parcel
from stogora_app.shipping.shipment import Shipment

a = Address('Steven', '1102 S Abel St.', 'Milpitas', 'California', '95035', 'United States')
b = Address('Other', '1880 N Capitol Ave', 'San Jose', 'California', None, 'United States')
b = b.verified_address()
a = a.verified_address()
p = Parcel(1, 2, 3, 4)

d = Shipment(a, b, p)
