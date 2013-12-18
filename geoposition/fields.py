from __future__ import unicode_literals

from django.db import models

from . import Geoposition
from .forms import GeopositionField as GeopositionFormField
from django.utils.encoding import smart_text


class GeopositionField(models.Field):
    description = "A geoposition (latitude and longitude)"
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 42
        if not 'default' in kwargs:
            kwargs['default'] = "0,0"
        super(GeopositionField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'CharField'

    def to_python(self, value):
        if not value:
            return Geoposition(0, 0)
        if isinstance(value, Geoposition):
            return value
        if isinstance(value, list):
            return Geoposition(value[0], value[1])

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

        return Geoposition(latitude, longitude)

    def get_prep_value(self, value):
        return str(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return smart_text(value)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': GeopositionFormField
        }
        defaults.update(kwargs)
        if not 'initial' in defaults or defaults['initial'] is None:
            defaults['initial'] = '0,0'
        return super(GeopositionField, self).formfield(**defaults)
