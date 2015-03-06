from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _

from .widgets import GeopositionWidget, GeopositionWithZoomWidget 
from . import Geoposition, GeopositionWithZoom


class GeopositionField(forms.MultiValueField):
    default_error_messages = {
        'invalid': _('Enter a valid geoposition.')
    }

    widget_class = GeopositionWidget

    object_class = Geoposition

    def __init__(self, *args, **kwargs):
        self.widget = self.widget_class()
        fields = self._get_fields()

        if 'initial' in kwargs:
            kwargs['initial'] = self.object_class(*kwargs['initial'].split(','))
        super(GeopositionField, self).__init__(fields, **kwargs)

    def _get_fields(self):
        return (
            forms.DecimalField(label=_('latitude')),
            forms.DecimalField(label=_('longitude')),
        )

    def widget_attrs(self, widget):
        classes = widget.attrs.get('class', '').split()
        classes.append('geoposition')
        return {'class': ' '.join(classes)}

    def compress(self, value_list):
        if value_list:
            return value_list
        return ""

class GeopositionWithZoomField(GeopositionField):
    widget_class = GeopositionWithZoomWidget
    object_class = GeopositionWithZoom
    def _get_fields(self):
        return (
            forms.DecimalField(label=_('latitude')),
            forms.DecimalField(label=_('longitude')),
            forms.IntegerField(label=_('zoom')),
        )

