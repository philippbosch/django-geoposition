.. include:: ../README.rst

Installation
------------

- Use your favorite Python packaging tool to install ``geoposition``
  from `PyPI`_, e.g.::

    pip install django-geoposition

- Add ``"geoposition"`` to your ``INSTALLED_APPS`` setting::

    INSTALLED_APPS = (
        # …
        "geoposition",
    )

- If you are still using Django <1.3, you are advised to install 
  `django-staticfiles`_ for static file serving.


Usage
-----

``django-geoposition`` comes with a model field that makes it pretty
easy to add a geoposition field to one of your models. To make use of
it:

- In your ``myapp/models.py``::

    from django.db import models
    from geoposition.fields import GeopositionField
    
    class PointOfInterest(models.Model):
        name = models.CharField(max_length=100)
        position = GeopositionField()

- This enables the following simple API::

    >>> from myapp.models import PointOfInterest
    >>> poi = PointOfInterest.objects.get(id=1)
    >>> poi.position
    Geoposition(52.522906,13.41156)
    >>> poi.position.latitude
    52.522906
    >>> poi.position.longitude
    13.41156


Form field and widget
---------------------

If you use a ``GeopositionField`` in a form (e.g. in the admin) it
will automatically show a `Google Maps`_ widget with a marker at the
currently stored position. You can drag and drop the marker with the
mouse and the corresponding latitude and longitude fields will be
updated accordingly.

It looks like this:

|geoposition-widget-admin|


Settings
--------

At the moment there are no settings, but I should propably add some …






.. _PyPI: http://pypi.python.org/pypi/django-geoposition
.. _django-staticfiles: http://github.com/jezdez/django-staticfiles
.. _Google Maps: http://code.google.com/apis/maps/documentation/javascript/
.. |geoposition-widget-admin| image:: images/geoposition-widget-admin.jpg
