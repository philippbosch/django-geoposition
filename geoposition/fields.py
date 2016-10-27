from __future__ import unicode_literals
from decimal import Decimal
import ast

from django.db import models
from django.utils import six
from django.utils.six import with_metaclass
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_text

from . import Geoposition
from .forms import GeopositionField as GeopositionFormField


class GeopositionField(models.Field):
    description = _("A geoposition (latitude and longitude)")

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 42
        super(GeopositionField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'CharField'

    def to_python(self, value):
        if not value or value == 'None':
            return None
        if isinstance(value, Geoposition):
            return value
        if isinstance(value, list):
            return Geoposition(value[0], value[1])

        try:
            dict_value = ast.literal_eval(value)
            if isinstance(dict_value, dict):

                if 'lat' in dict_value:
                    latitude = dict_value['lat']
                elif 'latitude' in dict_value:
                    latitude = dict_value['latitude']
                else:
                    latitude = '0.0'

                if 'lng' in dict_value:
                    longitude = dict_value['lng']
                elif 'longitude' in dict_value:
                    longitude = dict_value['longitude']
                else:
                    longitude = '0.0'

                return Geoposition(latitude, longitude)
        except:

            if isinstance(value, six.text_type):

                # default case is string
                value_parts = value.rsplit(',')

                try:
                    latitude = Decimal(value_parts[0])
                except:
                    latitude = '0.0'
                try:
                    longitude = Decimal(value_parts[1])
                except:
                    longitude = '0.0'

                return Geoposition(latitude, longitude)

        return Geoposition('0.0', '0.0')

    def from_db_value(self, value, expression, connection, context):
        return self.to_python(value)

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
        return super(GeopositionField, self).formfield(**defaults)

