from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

from .widgets import GeopositionWidget


@deconstructible
class NumberIsInRangeValidator(object):

    """
    Validator that tests if a value is in a range (inclusive).
    """

    def __init__(self, lower=None, upper=None, error_message=None):
        self.lower, self.upper = lower, upper
        if error_message is None or not error_message:
            if lower and upper:
                self.error_message = _("This value must be between %s and %s.") % (lower, upper)
            elif lower:
                self.error_message = _("This value must be at least %s.") % lower
            elif upper:
                self.error_message = _("This value must be no more than %s.") % upper
        else:
            self.error_message = error_message

    def __call__(self, field_data):
        # Try to make the value numeric. If this fails, we assume another
        # validator will catch the problem.
        try:
            val = float(field_data)
        except ValueError:
            return

        # Now validate
        if self.lower and self.upper and (val < self.lower or val > self.upper):
            raise ValidationError(self.error_message)
        elif self.lower and val < self.lower:
            raise ValidationError(self.error_message)
        elif self.upper and val > self.upper:
            raise ValidationError(self.error_message)


class GeopositionField(forms.MultiValueField):
    default_error_messages = {
        'invalid_latitude': _('Enter a valid value for latitude.'),
        'invalid_longitude': _('Enter a valid value for longitude.'),
        'invalid_elevation': _('Enter a valid value for elevation.'),
    }

    def __init__(self, *args, **kwargs):
        self.widget = GeopositionWidget()
        errors = self.default_error_messages.copy()

        if 'error_messages' in kwargs:
            errors.update(kwargs['error_messages'])

        localize = kwargs.get('localize', False)

        fields = (
            forms.FloatField(
                label=_('latitude'),
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
            forms.FloatField(
                label=_('longitude'),
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
            forms.FloatField(
                label=_('elevation'),
                error_messages={'invalid': errors['invalid_elevation']},
                localize=localize
            ),
        )
        super(GeopositionField, self).__init__(fields, **kwargs)

    def widget_attrs(self, widget):
        classes = widget.attrs.get('class', '').split()
        classes.append('geoposition')
        return {'class': ' '.join(classes)}

    def compress(self, value_list):
        if value_list:
            return value_list
        return ""
