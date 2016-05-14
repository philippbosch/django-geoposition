from __future__ import unicode_literals

from decimal import Decimal

# Versioning
VERSION = (0, 2, 2)
__version__ = '.'.join(map(str, VERSION))


# Loads GeopositionConfig
default_app_config = 'geoposition.apps.GeopositionConfig'


# Geoposition object with optional elevation property
# * Please use elevation considering that it is always in meters
class Geoposition(object):

    def __init__(self, latitude=0, longitude=0, elevation=0, use_elevation=False):
        self._use_elevation = bool(use_elevation)

        if isinstance(latitude, float) or isinstance(latitude, int):
            latitude = str(latitude)

        if isinstance(longitude, float) or isinstance(longitude, int):
            longitude = str(longitude)

        if isinstance(elevation, float) or isinstance(elevation, int):
            elevation = str(elevation)

        self._latitude = Decimal(latitude)
        self._longitude = Decimal(longitude)
        self._elevation = Decimal(elevation)

    # The property 'use_elevation' is not editable
    @property
    def use_elevation(self):
        return self._use_elevation

    # Getter, setter, and deleter for 'latitude' property
    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        self._latitude = value

    @latitude.deleter
    def latitude(self):
        del self._latitude

    # Getter, setter, and deleter for 'longitude' property
    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        self._longitude = value

    @longitude.deleter
    def longitude(self):
        del self._longitude

    # Getter, setter, and deleter for 'latitude' property
    @property
    def elevation(self):
        if self.use_elevation:
            return self._elevation

        return None

    @elevation.setter
    def elevation(self, value):
        if self.use_elevation:
            self._elevation = value

    @elevation.deleter
    def elevation(self):
        del self._elevation

    # Override default functions and operators
    def __dict__(self):
        geo_dict = dict(
            lat=self.latitude,
            lng=self.longitude,
        )

        if self.use_elevation:
            geo_dict.update(
                dict(
                    elv=self.elevation
                )
            )

        return geo_dict

        return None

    def __str__(self):
        if self.use_elevation:
            return "{lat},{lng},{elv}".format(**self.__dict__())

        return "{lat},{lng}".format(**self.__dict__())

    def __repr__(self):
        return "Geoposition({0})".format(self)

    def __len__(self):
        return len(str(self))

    def __eq__(self, other):
        return (isinstance(other, Geoposition) and
                self.latitude == other.latitude and
                self.longitude == other.longitude and
                self.elevation == other.elevation)

    def __ne__(self, other):
        return (not isinstance(other, Geoposition) or
                self.latitude != other.latitude or
                self.longitude != other.longitude or
                self.elevation != other.elevation)
