from django import forms
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape
import re
import json

def flat_data_att(attrs):
    """
    Convert a dictionary of attributes to a single string.
    The returned string will contain a leading space followed by key="value",
    XML-style pairs.  It is assumed that the keys do not need to be XML-escaped.
    If the passed dictionary is empty, then return an empty string.
    If value contains a dictionnary, it is written as key='value' and is not
    escaped.
    """
    return u''.join(
        [u' %s="%s"' % (k, conditional_escape(v)) for k, v in attrs.items() if not isinstance(v, dict)]
    ) + u''.join(
        [u" %s='%s'" % (k, json.dumps(v)) for k, v in attrs.items() if isinstance(v, dict)]
    )

class MapWidget(forms.Widget):
    
    def __init__(self, attrs=None, mapOptions=None,
                 latitude_selector='div[class="form-row latitude"]',
                 longitude_selector='div[class="form-row longitude"]'):
        super(MapWidget,self).__init__(attrs)
        self.latitude_selector = latitude_selector
        self.longitude_selector = longitude_selector
        self.mapOptions = mapOptions or {}
    
    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs)
        
        final_attrs['data-map-widget'] = {
            'latitudeSelector': self.latitude_selector,
            'longitudeSelector': self.longitude_selector,
            'mapOptions': self.mapOptions,
        }
        return mark_safe(u'<p%s></p>' % flat_data_att(final_attrs))
    
    class Media:
        js = ('geoposition/geoposition.js',)
        css = {
            'all': ('geoposition/geoposition.css',)
    }

class GeopositionWidget(forms.MultiWidget):
    def __init__(self, attrs=None, mapOptions=None):
        widgets = (
            forms.TextInput(),
            forms.TextInput(),
        )
        super(GeopositionWidget, self).__init__(widgets, attrs)
        self.mapOptions = mapOptions or {}
    
    def decompress(self, value):
        if value:
            return [value.latitude, value.longitude]
        return [None,None]
    
    def format_output(self, rendered_widgets):
        attributes = { 'data-map-widget':{
            'latitudeSelector': '#' + re.search('id="([^"]+)"',rendered_widgets[0]).group(1),
            'longitudeSelector': '#' + re.search('id="([^"]+)"',rendered_widgets[1]).group(1),
            'mapOptions': self.mapOptions,
        }}
        return render_to_string('geoposition/widgets/geoposition.html', {
            'attributes': mark_safe(flat_data_att(attributes)),
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