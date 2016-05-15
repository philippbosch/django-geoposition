from __future__ import unicode_literals

import json
from django import forms
from django.template.loader import render_to_string
from django.utils import six
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _
from geoposition.conf import settings


class GeopositionWidget(forms.MultiWidget):

    def __init__(self, attrs={}):
        self._use_elevation = attrs.get('use_elevation', False)

        if 'use_elevation' in attrs:
            del attrs['use_elevation']

        widgets = (
            forms.TextInput(),
            forms.TextInput(),
            forms.TextInput(),
        )

        super(GeopositionWidget, self).__init__(widgets, attrs)

    @property
    def use_elevation(self):
        return self._use_elevation

    def decompress(self, value):
        if isinstance(value, six.text_type):
            return value.rsplit(',')

        if value:
            if value.use_elevation:
                return [value.latitude, value.longitude, value.elevation]
            else:
                return [value.latitude, value.longitude]

        return [0, 0, 0]

    def format_output(self, rendered_widgets):
        return render_to_string('geoposition/widgets/geoposition.html', {
            'latitude': {
                'html': rendered_widgets[0],
                'label': _("latitude"),
                'required': 'required' if self.is_required else '',
            },
            'longitude': {
                'html': rendered_widgets[1],
                'label': _("longitude"),
                'required': 'required' if self.is_required else '',
            },
            'elevation': {
                'html': mark_safe(rendered_widgets[2].replace('required', 'required' if self.is_required and self.use_elevation else '')),
                'label': _("elevation"),
                'required': 'required' if self.is_required and self.use_elevation else '',
                'hidden': '' if self.use_elevation else 'hidden'
            },
            'config': {
                'map_widget_height': settings.GEOPOSITION_MAP_WIDGET_HEIGHT,
                'map_options': json.dumps(settings.GEOPOSITION_MAP_OPTIONS),
                'marker_options': json.dumps(settings.GEOPOSITION_MARKER_OPTIONS),
            }
        })

    class Media:
        js = (
            '//maps.google.com/maps/api/js?',
            'geoposition/geoposition.js',
        )
        css = {
            'all': ('geoposition/geoposition.css',)
        }
