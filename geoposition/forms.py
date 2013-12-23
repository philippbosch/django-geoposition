from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _

from .widgets import GeopositionWidget
from . import Geoposition


class GeopositionField(forms.MultiValueField):
    default_error_messages = {
        'invalid': _('Enter a valid geoposition.')
    }

    def __init__(self, *args, **kwargs):
        self.widget = GeopositionWidget()
        fields = (
            forms.DecimalField(label=_('latitude')),
            forms.DecimalField(label=_('longitude')),
        )
        if 'initial' in kwargs:
            kwargs['initial'] = Geoposition(*kwargs['initial'].split(','))
        super(GeopositionField, self).__init__(fields, **kwargs)

    def widget_attrs(self, widget):
        classes = widget.attrs.get('class', '').split()
        classes.append('geoposition')
        return {'class': ' '.join(classes)}

    def compress(self, value_list):
        if value_list:
            return value_list
        return ""
