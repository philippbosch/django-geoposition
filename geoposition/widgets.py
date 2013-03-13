from django import forms
from django.template.loader import render_to_string
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
            'settings': {
                'zoom': settings.GEOPOSITION_DEFAULT_ZOOM,
                'lat': settings.GEOPOSITION_DEFAULT_CENTRE[0],
                'long': settings.GEOPOSITION_DEFAULT_CENTRE[1],
            },
        })
    
    class Media:
        js = ('geoposition/geoposition.js',)
        css = {
            'all': ('geoposition/geoposition.css',)
        }
