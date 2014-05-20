from __future__ import unicode_literals

import json
from django import forms
from django.template.loader import render_to_string
from django.utils import six
from django.utils.translation import ugettext_lazy as _
from .conf import settings


class GeopositionWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = (
            forms.TextInput(),
            forms.TextInput(),
        )
        super(GeopositionWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if isinstance(value, six.text_type):
            return value.rsplit(',')
        if value:
            return [value.latitude, value.longitude]
        return [None,None]

    def format_output(self, rendered_widgets):
        return render_to_string('geoposition/widgets/geoposition.html', {
            'latitude': {
                'html': rendered_widgets[0],
                'label': _("latitude"),
            },
            'longitude': {
                'html': rendered_widgets[1],
                'label': _("longitude"),
            },
            'config': {
                'map_widget_height': settings.GEOPOSITION_MAP_WIDGET_HEIGHT,
                'map_options': json.dumps(settings.GEOPOSITION_MAP_OPTIONS),
                'marker_options': json.dumps(settings.GEOPOSITION_MARKER_OPTIONS),
            }
        })

    class Media:
        js = (
            '//maps.google.com/maps/api/js?sensor=false',
            'geoposition/geoposition.js',
        )
        css = {
            'all': ('geoposition/geoposition.css',)
        }
