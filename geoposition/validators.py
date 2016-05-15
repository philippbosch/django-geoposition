from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

from decimal import Decimal


@deconstructible
class NumberIsInRangeValidator(object):

    """
    Validator that tests if a value is in a range (inclusive).
    """

    def __init__(self, lower=None, upper=None, error_message=None):
        self.lower, self.upper = Decimal(lower), Decimal(upper)
        if error_message is None or not error_message:
            if lower and upper:
                self.error_message = _("This value must be between %(lower)s and %(upper)s.") % (lower, upper)
            elif lower:
                self.error_message = _("This value must be at least %(lower)s.") % lower
            elif upper:
                self.error_message = _("This value must be no more than %(upper)s.") % upper
        else:
            self.error_message = error_message

    def __call__(self, field_data):
        # Try to make the value numeric. If this fails, we assume another
        # validator will catch the problem.
        try:
            val = Decimal(field_data)
        except ValueError:
            return

        # Now validate
        if self.lower and self.upper and (val < self.lower or val > self.upper):
            raise ValidationError(self.error_message)
        elif self.lower and val < self.lower:
            raise ValidationError(self.error_message)
        elif self.upper and val > self.upper:
            raise ValidationError(self.error_message)
