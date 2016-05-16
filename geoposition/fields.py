from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_text

from . import Geoposition
from .forms import GeopositionField as GeopositionFormField


class GeopositionField(models.Field):
    description = _("A geoposition field to store latitude, longitude and elevation data")

    def __init__(self, use_elevation=False, *args, **kwargs):
        kwargs['max_length'] = 128

        self._use_elevation = use_elevation

        super(GeopositionField, self).__init__(*args, **kwargs)

    @property
    def use_elevation(self):
        return self._use_elevation

    def deconstruct(self):
        name, path, args, kwargs = super(GeopositionField, self).deconstruct()
        kwargs['use_elevation'] = self.use_elevation

        return name, path, args, kwargs

    def get_internal_type(self):
        return 'CharField'

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value

        value_parts = value.rsplit(',')

        try:
            latitude = value_parts[0]
        except IndexError:
            latitude = '0'
        try:
            longitude = value_parts[1]
        except IndexError:
            longitude = '0'
        try:
            elevation = value_parts[2]
        except IndexError:
            elevation = '0'

        return Geoposition(latitude=latitude,
                           longitude=longitude,
                           elevation=elevation,
                           use_elevation=self.use_elevation)

    def to_python(self, value):
        if not value or value == 'None':
            return None

        if isinstance(value, Geoposition):
            return value

        if isinstance(value, list):
            if self.use_elevation:
                return Geoposition(latitude=value[0],
                                   longitude=value[1],
                                   elevation=value[2],
                                   use_elevation=self.use_elevation)

            return Geoposition(latitude=value[0],
                               longitude=value[1],
                               elevation='0',
                               use_elevation=self.use_elevation)

        # default case is string
        value_parts = value.rsplit(',')

        try:
            latitude = value_parts[0]
        except IndexError:
            latitude = '0.0'

        try:
            longitude = value_parts[1]
        except IndexError:
            longitude = '0.0'

        try:
            elevation = value_parts[2]
        except IndexError:
            elevation = '0.0'

        return Geoposition(
            latitude=latitude,
            longitude=longitude,
            elevation=elevation,
            use_elevation=self.use_elevation
        )

    def get_prep_value(self, value):
        return str(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return smart_text(value)

    def formfield(self, **kwargs):
        defaults = dict(
            form_class=GeopositionFormField,
            use_elevation=self.use_elevation,
        )

        defaults.update(kwargs)

        return super(GeopositionField, self).formfield(**defaults)
