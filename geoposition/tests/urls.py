from django.urls import path, include
from django.contrib import admin
from example.views import poi_list

admin.autodiscover()

urlpatterns = [
    path('', poi_list),
    path('admin/', admin.site.urls),
]
