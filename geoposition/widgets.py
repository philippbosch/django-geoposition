from __future__ import unicode_literals
from copy import deepcopy

import json
import re

from django import forms
from django.template.loader import render_to_string
from django.utils import six
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from .conf import settings


class GeopositionWidget(forms.MultiWidget):
    map_options = {}

    def __init__(self, attrs=None, map_options=None):
        widgets = (
            forms.TextInput(),
            forms.TextInput(),
        )
        self.map_options = map_options or {}
        super(GeopositionWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if isinstance(value, six.text_type):
            return value.rsplit(',')
        if value:
            return [value.latitude, value.longitude]
        return [None, None]

    def format_output(self, rendered_widgets):
        options = deepcopy(settings.GEOPOSITION_MAP_OPTIONS)
        options.update(self.map_options)
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
                'latitude_selector': '#' + re.search('id="([^"]+)"', rendered_widgets[0]).group(1),
                'longitude_selector': '#' + re.search('id="([^"]+)"', rendered_widgets[1]).group(1),
                'map_widget_height': settings.GEOPOSITION_MAP_WIDGET_HEIGHT,
                'map_options': json.dumps(options),
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

