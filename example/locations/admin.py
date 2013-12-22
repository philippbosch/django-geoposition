from django.contrib import admin
from .models import PointOfInterest


class PointOfInterestAdmin(admin.ModelAdmin):
    list_display = ('name', 'position',)


admin.site.register(PointOfInterest, PointOfInterestAdmin)
