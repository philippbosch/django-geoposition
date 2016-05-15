# -*- coding: utf-8 -*-
from django.conf import settings
from appconf import AppConf


class GeopositionConf(AppConf):
    MAP_WIDGET_HEIGHT = 400
    MAP_OPTIONS = {}
    MAP_TYPE = "ROADMAP"
    MARKER_OPTIONS = {}

    class Meta:
        prefix = 'geoposition'
