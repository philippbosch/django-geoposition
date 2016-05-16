from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class GeosampleConfig(AppConfig):
    name = 'geosample'
    verbose_name = _('Geoposition Sample Application')

    label = 'geosample'
