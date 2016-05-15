from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _
from geoposition.validators import NumberIsInRangeValidator
from geoposition.widgets import GeopositionWidget


class GeopositionField(forms.MultiValueField):
    default_error_messages = {
        'invalid_latitude': _('Enter a valid value for latitude.'),
        'invalid_longitude': _('Enter a valid value for longitude.'),
        'invalid_elevation': _('Enter a valid value for elevation.'),
    }

    def __init__(self, *args, **kwargs):
        kwargs['required'] = kwargs.get('required', True)

        self._use_elevation = kwargs.get('use_elevation', False)

        if 'use_elevation' in kwargs:
            del kwargs['use_elevation']

        attrs = dict(
            required=True,
            use_elevation=self._use_elevation
        )

        self.widget = GeopositionWidget(attrs=attrs)

        errors = self.default_error_messages.copy()

        if 'error_messages' in kwargs:
            errors.update(kwargs['error_messages'])

        localize = kwargs.get('localize', False)

        fields = (
            forms.DecimalField(
                label=_('latitude'),
                required=kwargs.get('required', True),
                error_messages={'invalid': errors['invalid_latitude']},
                localize=localize,
                validators=[
                    NumberIsInRangeValidator(
                        lower=-90.0,
                        upper=+90.0,
                        error_message=_("latitude must be a value between -90 and +90 degrees").capitalize()
                    )
                ]
            ),
            forms.DecimalField(
                label=_('longitude'),
                required=kwargs.get('required', True),
                error_messages={'invalid': errors['invalid_longitude']},
                localize=localize,
                validators=[
                    NumberIsInRangeValidator(
                        lower=-180.0,
                        upper=+180.0,
                        error_message=_("longitude must be a value between -180 and +180 degrees").capitalize()
                    ),
                ]
            ),
            forms.DecimalField(
                label=_('elevation'),
                required=kwargs.get('required', True) and self.use_elevation,
                error_messages={'invalid': errors['invalid_elevation']},
                localize=localize,
            ),
        )

        super(GeopositionField, self).__init__(fields, **kwargs)

    @property
    def use_elevation(self):
        return self._use_elevation

    def widget_attrs(self, widget):
        classes = widget.attrs.get('class', '').split()
        classes.append('geoposition')

        return {'class': ' '.join(classes)}

    def compress(self, value_list):
        if value_list:
            return value_list
        return ""
