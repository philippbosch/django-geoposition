from __future__ import unicode_literals
from decimal import Decimal, DecimalException

default_app_config = 'geoposition.apps.GeoPositionConfig'

VERSION = (0, 3, 1)
__version__ = '.'.join(map(str, VERSION))


class Geoposition(object):
    def __init__(self, latitude, longitude):
        if isinstance(latitude, float) or isinstance(latitude, int):
            latitude = str(latitude)
            
        if isinstance(longitude, float) or isinstance(longitude, int):
            longitude = str(longitude)

        try:
            self.latitude = Decimal(latitude)
        except DecimalException:
            self.latitude = '0.0'

        try:
            self.longitude = Decimal(longitude)
        except DecimalException:
            self.longitude = '0.0'

    def __str__(self):
        return "%s,%s" % (self.latitude, self.longitude)

    def __repr__(self):
        return "Geoposition(%s)" % str(self)

    def __len__(self):
        return len(str(self))

    def __eq__(self, other):
        return isinstance(other, Geoposition) and self.latitude == other.latitude and self.longitude == other.longitude

    def __ne__(self, other):
        return not isinstance(other, Geoposition) or self.latitude != other.latitude or self.longitude != other.longitude
