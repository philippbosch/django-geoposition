from django import forms
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from . import Geoposition


class GeopositionWidget(forms.MultiWidget):
    def __init__(self, attrs=None, template=None):
        default_template = 'geoposition/widgets/geoposition.html'
        self.template = template or default_template

        widgets = (
            forms.TextInput(),
            forms.TextInput(),
        )
        super(GeopositionWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        self.initial = False
        if value:
            if isinstance(value, Geoposition):
                return [value.latitude, value.longitude]
            else:
                # Initial value
                self.initial = True
                value = str(value)
                return value.split(',')

        return [None, None]

    def format_output(self, rendered_widgets):
        context = {
            'initial': self.initial if hasattr(self, 'initial') else None,
            'latitude': {
                'html': rendered_widgets[0],
                'label': _("latitude"),
            },
            'longitude': {
                'html': rendered_widgets[1],
                'label': _("longitude"),
            },
        }
        return render_to_string(self.template, context)

    class Media:
        js = ('geoposition/geoposition.js',)
        css = {
            'all': ('geoposition/geoposition.css',)
        }
