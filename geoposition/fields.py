from __future__ import unicode_literals

from django.db import models
from django.utils.six import with_metaclass
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_text

from . import Geoposition
from .forms import GeopositionField as GeopositionFormField


class CastOnAssignDescriptor(object):
    """
    A property descriptor which ensures that `field.to_python()` is called on _every_ assignment to the field.

    This used to be provided by the `django.db.models.subclassing.Creator` class, which in turn
    was used by the deprecated-in-Django-1.10 `SubfieldBase` class, hence the reimplementation here.
    """

    def __init__(self, field):
        self.field = field

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        return obj.__dict__[self.field.name]

    def __set__(self, obj, value):
        obj.__dict__[self.field.name] = self.field.to_python(value)


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

    def contribute_to_class(self, cls, name):
        super(GeopositionField, self).contribute_to_class(cls, name)
        setattr(cls, name, CastOnAssignDescriptor(self))

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
