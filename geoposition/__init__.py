from __future__ import unicode_literals

from decimal import Decimal

VERSION = (0, 2, 2)
__version__ = '.'.join(map(str, VERSION))


class Geoposition(object):

    def __init__(self, latitude, longitude, elevation):
        if isinstance(latitude, float) or isinstance(latitude, int):
            latitude = str(latitude)
        if isinstance(longitude, float) or isinstance(longitude, int):
            longitude = str(longitude)
        if isinstance(elevation, float) or isinstance(elevation, int):
            elevation = str(elevation)

        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.elevation = float(elevation)

    def __str__(self):
        return "%s,%s,%s" % (self.latitude, self.longitude, self.elevation)

    def __repr__(self):
        return "Geoposition(%s)" % str(self)

    def __len__(self):
        return len(str(self))

    def __eq__(self, other):
        return isinstance(other, Geoposition) and self.latitude == other.latitude and self.longitude == other.longitude and self.elevation == other.elevation

    def __ne__(self, other):
        return not isinstance(other, Geoposition) or self.latitude != other.latitude or self.longitude != other.longitude or self.elevation != other.elevation
