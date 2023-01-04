from __future__ import absolute_import
from django.db import models

from . import Geoposition
from .forms import GeopositionField as GeopositionFormField
from django.utils.encoding import smart_text
import decimal
import six


class GeopositionField(models.Field):
    description = "A geoposition (latitude and longitude)"
    
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 42
        super(GeopositionField, self).__init__(*args, **kwargs)
    
    def get_internal_type(self):
        return 'CharField'
    
    def to_python(self, value):
        if not value:
            return None
        if isinstance(value, Geoposition):
            return value
        if isinstance(value, list) or isinstance(value, tuple):
            return Geoposition(value[0], value[1])
        
        value_parts = value.rsplit(',')
        try:
            latitude = value_parts[0]
        except IndexError:
            return None
        try:
            longitude = value_parts[1]
        except IndexError:
            return None
        
        try:
            return Geoposition(latitude, longitude)
        except decimal.InvalidOperation:
            return None

    def from_db_value(self, value, expression, connection, context=None):
        return self.to_python(value)
    
    def get_prep_value(self, value):
        return six.text_type(value)
    
    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return smart_unitext(value)
    
    def formfield(self, **kwargs):
        defaults = {
            'form_class': GeopositionFormField
        }
        defaults.update(kwargs)
        return super(GeopositionField, self).formfield(**defaults)
        
try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^geoposition\.fields\.GeopositionField"])
except ImportError:
    pass
