from django.urls import path
from django.contrib import admin

from example import views

admin.autodiscover()

urlpatterns = [
    path('', views.poi_list),
    path('admin/', admin.site.urls)
]
