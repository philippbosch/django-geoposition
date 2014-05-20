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

Admin
^^^^^

If you use a ``GeopositionField`` in the admin it will automatically
show a `Google Maps`_ widget with a marker at the currently stored
position. You can drag and drop the marker with the mouse and the
corresponding latitude and longitude fields will be updated
accordingly.

It looks like this:

|geoposition-widget-admin|


Regular Forms
^^^^^^^^^^^^^

Using the map widget on a regular form outside of the admin requires
just a little more work. In your template make sure that

- `jQuery`_ is included
- the static files (JS, CSS) of the map widget are included (just use
  ``{{ form.media }}``)

**Example**::

    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.8/jquery.min.js"></script>
    <form method="POST" action="">{% csrf_token %}
        {{ form.media }}
        {{ form.as_p }}
    </form>


Settings
--------

You can customize the `MapOptions`_ and `MarkerOptions`_ used to initialize the
map and marker in JavaScript by defining a ``GEOPOSITION_MAP_OPTIONS`` or
``GEOPOSITION_MARKER_OPTIONS`` in your ``settings.py``.

**Example**::

    GEOPOSITION_MAP_OPTIONS = {
        'minZoom': 3,
        'maxZoom': 15,
    }

    GEOPOSITION_MARKER_OPTIONS = {
        'cursor': 'move'
    }


You can also customize the height of the displayed map widget by setting
``GEOPOSITION_MAP_WIDGET_HEIGHT`` to an integer value (default is 480).



.. _PyPI: http://pypi.python.org/pypi/django-geoposition
.. _django-staticfiles: http://github.com/jezdez/django-staticfiles
.. _Google Maps: http://code.google.com/apis/maps/documentation/javascript/
.. |geoposition-widget-admin| image:: images/geoposition-widget-admin.jpg
.. _jQuery: http://jquery.com
.. _MapOptions: https://developers.google.com/maps/documentation/javascript/reference?csw=1#MapOptions
.. _MarkerOptions: https://developers.google.com/maps/documentation/javascript/reference?csw=1#MarkerOptions
