from __future__ import unicode_literals

import json
from django import forms
from django.template.loader import render_to_string
from django.utils import six
from django.utils.translation import ugettext_lazy as _
from .conf import settings


class GeopositionWidget(forms.MultiWidget):
    def __init__(self, attrs):
        #self.hide_coords = (attrs is not None) and isinstance(attrs, dict) and (attrs.pop('hide_coords', False))
        self.hide_coords = attrs.pop('hide_coords')
        if self.hide_coords:
            widgets = [
                forms.HiddenInput(),
                forms.HiddenInput(),
            ]
        else:
            widgets = [
                forms.TextInput(),
                forms.TextInput(),
            ]

        self.get_address_line = attrs.pop('get_address_line')
        if self.get_address_line:
            widgets.append(forms.HiddenInput())

        super(GeopositionWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if isinstance(value, six.text_type):
            return value.rsplit(',')
        if value:
            return [value.latitude, value.longitude]
        return [None, None]

    def format_output(self, rendered_widgets):
        options = {'show_coords': not self.hide_coords,
                    'latitude'   : {'html': rendered_widgets[0], 'label': _("latitude"), },
                    'longitude'  : {'html': rendered_widgets[1], 'label': _("longitude"), },
                    'config'     : {'map_widget_height' : settings.MAP_WIDGET_HEIGHT or 500,
                                    'map_options'       : json.dumps(settings.MAP_OPTIONS),
                                    'marker_options'    : json.dumps(settings.MARKER_OPTIONS),}}

        options['address_line'] = {'html': rendered_widgets[2] if self.get_address_line else ""}
        return render_to_string('geoposition/widgets/geoposition.html', options)

    class Media:
        js = (
            '//maps.google.com/maps/api/js?key=%s' % settings.GOOGLE_MAPS_API_KEY,
            'geoposition/geoposition.js',
        )
        css = {
            'all': ('geoposition/geoposition.css',)
        }
