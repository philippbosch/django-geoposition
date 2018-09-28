from django.core.validators import RegexValidator
from django.db import models
from django.utils.text import slugify

from geoposition.fields import GeopositionField


class PointOfInterest(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=10)
    position = GeopositionField(blank=True)

    class Meta:
        verbose_name_plural = 'points of interest'


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    position = GeopositionField(blank=True)
