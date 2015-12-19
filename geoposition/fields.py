from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_text

from . import Geoposition
from .forms import GeopositionField as GeopositionFormField


class GeopositionField(models.Field):
    description = _("A geoposition field to store latitude, longitude and elevation data")

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 42
        super(GeopositionField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'CharField'

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value

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

        return Geoposition(latitude, longitude, elevation)

    def to_python(self, value):
        if not value or value == 'None':
            return None
        if isinstance(value, Geoposition):
            return value
        if isinstance(value, list):
            return Geoposition(value[0], value[1], value[2])

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

        return Geoposition(latitude, longitude, elevation)

    def get_prep_value(self, value):
        return str(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return smart_text(value)

    def formfield(self, **kwargs):
        defaults = {'form_class': GeopositionFormField}
        defaults.update(kwargs)
        return super(GeopositionField, self).formfield(**defaults)
