from __future__ import unicode_literals

from django.db import models
from django.utils.six import with_metaclass
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_text

from . import Geoposition, GeopositionWithZoom
from .forms import GeopositionField as GeopositionFormField, GeopositionWithZoomField as GeopositionWithZoomFormField


class GeopositionField(with_metaclass(models.SubfieldBase, models.Field)):
    description = _("A geoposition (latitude and longitude)")

    object_class = Geoposition

    formfield_class = GeopositionFormField

    defaults = ('0.0', '0.0',)

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 42
        super(GeopositionField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'CharField'

    def _set_default_values(self, value_parts):
        for i, d in enumerate(self.defaults):
            try:
                value_parts[i]
            except IndexError:
                value_parts.append(d)

        return value_parts

    def to_python(self, value):
        if not value or value == 'None':
            return None
        if isinstance(value, self.object_class):
            return value
        if isinstance(value, list):
            return self.object_class(*value)

        # default case is string
        value_parts = value.split(',')
        # Set default values if not found
        value_parts = self._set_default_values(value_parts)

        return self.object_class(*value_parts)

    def get_prep_value(self, value):
        return str(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return smart_text(value)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': self.formfield_class
        }
        defaults.update(kwargs)
        return super(GeopositionField, self).formfield(**defaults)

class GeopositionWithZoomField(GeopositionField):
    description = _("A geoposition (latitude, longitude and zoom)")

    object_class = GeopositionWithZoom

    formfield_class = GeopositionWithZoomFormField

    defaults = ('0.0', '0.0', 8)

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 45
        super(GeopositionWithZoomField, self).__init__(*args, **kwargs)
