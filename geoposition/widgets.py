from django import forms
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _


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
        if value:
            try:
                return [value.latitude, value.longitude]
            except AttributeError:
                # Value is not Geoposition instance
                # try to split it by comma
                value = str(value)
                return value.split(',')
        return [None, None]

    def format_output(self, rendered_widgets):
        return render_to_string(self.template, {
            'latitude': {
                'html': rendered_widgets[0],
                'label': _("latitude"),
            },
            'longitude': {
                'html': rendered_widgets[1],
                'label': _("longitude"),
            },
        })

    class Media:
        js = ('geoposition/geoposition.js',)
        css = {
            'all': ('geoposition/geoposition.css',)
        }
