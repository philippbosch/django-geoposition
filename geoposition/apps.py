from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class GeopositionConfig(AppConfig):
    name = 'geoposition'
    verbose_name = _('Geoposition')

    label = 'geoposition'
