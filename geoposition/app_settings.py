from __future__ import unicode_literals
from django.conf import settings

GEOPOSITION_GMAP_URL = getattr(settings, 'GEOPOSITION_GMAP_URL', '')
GEOPOSITION_GMAP_URL_AUTOLOAD = getattr(settings, 'GEOPOSITION_GMAP_URL_AUTOLOAD', True)

