from django.conf.urls import include, url
from django.contrib import admin
from example.views import poi_list

admin.autodiscover()

urlpatterns = [
    url(r'^$', poi_list),
    url(r'^admin/', include(admin.site.urls)),
]
