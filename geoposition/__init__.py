from __future__ import unicode_literals

from decimal import Decimal
from django.contrib.gis.geos import GEOSGeometry

VERSION = (0, 2, 2)
__version__ = '.'.join(map(str, VERSION))


class Geoposition(object):
    def __init__(self, latitude, longitude, altitude=None):
        if isinstance(latitude, float) or isinstance(latitude, int):
            latitude = str(latitude)
        if isinstance(longitude, float) or isinstance(longitude, int):
            longitude = str(longitude)
        if isinstance(altitude, float) or isinstance(altitude, int):
            altitude = str(altitude)

        self.latitude = Decimal(latitude)
        self.longitude = Decimal(longitude)
        self.altitude = Decimal(altitude) if not altitude is None else None

    def __str__(self):
        r =  "%s,%s" % (self.latitude, self.longitude)
        if not self.altitude is None:
            return "%s,%s" % (r, self.altitude)
        return r

    def __repr__(self):
        return "Geoposition(%s)" % str(self)

    def __len__(self):
        return len(str(self))

    def __eq__(self, other):
        return (isinstance(other, Geoposition) and self.latitude == other.latitude
                and self.longitude == other.longitude and self.altitude == other.altitude)

    def __ne__(self, other):
        return (not isinstance(other, Geoposition) or self.latitude != other.latitude
                or self.longitude != other.longitude or self.altitude != other.altitude)
