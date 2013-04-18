from django.conf import settings
from appconf import AppConf


class GeoPositionAppConf(AppConf):
    DEFAULT_ZOOM = 15
    DEFAULT_CENTRE = (0, 0,)

    class Meta:
        prefix = "GEOPOSITION"
