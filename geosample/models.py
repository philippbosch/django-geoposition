from django.utils.translation import ugettext as _

from django.db import models

from geoposition.fields import GeopositionField


class PointOfInterest(models.Model):
    name = models.CharField(
        _("name"),
        max_length=100
    )

    address = models.CharField(
        _("address"),
        max_length=255
    )

    city = models.CharField(
        _("city"),
        max_length=50
    )

    zipcode = models.CharField(
        _("zip code"),
        max_length=10
    )

    position = GeopositionField(
        name=_("position"),
        use_elevation=True
    )

    class Meta:
        verbose_name = _('Point of interest')
        verbose_name_plural = _('Points of interest')
