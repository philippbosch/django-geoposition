from __future__ import absolute_import
from decimal import Decimal
from six.moves import map
import six

VERSION = (0, 1, 4)
__version__ = '.'.join(map(str, VERSION))


class Geoposition(object):
    def __init__(self, latitude, longitude):

        self.latitude = latitude
        self.longitude = longitude


    @property
    def longitude(self):
        return self._longitude
    @longitude.setter
    def longitude(self, value):
        if isinstance(value, float) or isinstance(value, int):
            value = str(value)
        self._longitude = Decimal(value)

    @property
    def latitude(self):
        return self._latitude
    @latitude.setter
    def latitude(self, value):
        if isinstance(value, float) or isinstance(value, int):
            value = str(value)
        self._latitude = Decimal(value)

    @property
    def lat(self):
        return self._latitude
    @lat.setter
    def lat(self, value):
        self.latitude = value

    @property
    def long(self):
        return self._longitude
    @long.setter
    def long(self, value):
        self.longitude = value

    def __unicode__(self):
        return "%s,%s" % (self._latitude, self._longitude)
    
    def __repr__(self):
        return "Geoposition(%s)" % self.__unicode__()
    
    def __len__(self):
        return len(six.text_type(self))

    def __iter__(self):
        yield self._latitude
        yield self._longitude

    def __getitem__(self, key):
        if key == 0:
            return self._latitude
        elif key == 1:
            return self._longitude
        raise KeyError

    def __setitem__(self, key, value):
        if key == 0:
            self.latitude = value
        elif key == 1:
            self.longitude = value
        else:
            raise KeyError
