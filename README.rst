==================
django-geoposition
==================

A model field that can hold a geoposition (latitude/longitude), and corresponding admin widget.

This fork allow to pass some mapOptions to the GeopositionWidget::

    map = GeopositionField(widget=GeopositionWidget(mapOptions={
        'scrollwheel': False,
    }), required=False)

The HTML markup makes use of html5 data-map-widget attribute to pass the options, here is the generated HTML for the preceding formfield::

    <p  data-map-widget='{"mapOptions": {"scrollwheel": false}, "longitudeSelector": "#id_map_1", "latitudeSelector": "#id_map_0"}'></p>


Alternatively if you don't want to use a GeopositionField in your model, you can simply do::

    map = Field(widget=MapWidget(mapOptions={
        'scrollwheel': False,
    }), required=False)

This will reuse the latitude and longitude field from your model and the generated HTML will be::

    <p id="id_map" data-map-widget='{"mapOptions": {"scrollwheel": false}, "longitudeSelector": "div[class^=\"form-row\"][class~=\"longitude\"]", "latitudeSelector": "div[class^=\"form-row\"][class~=\"latitude\"]"}'></p>



----------
Parameters
----------
**GeopositionWidget** accepts only one parameter:  mapOtions. The camelCase form is here to remind you that this will
be pass to the javascript part of the widget, simply by dumping the mapOptions dict into a json string.

**MapWidget** accepts two more parameters: latitudeSelector and longitudeSelector, once again, camelCase because those
selectors will be passed to jQuery as selectors. They are optionnals and not needed if you fields are called latitude
and longitude.

The javascript side of the widget move the latitude and longitude imputs just above the map, that why we are passing
not the latitude's input id as selector but the formfield row.

EXAMPLE: If your model fields are called lat and lon, then you need to write::

    map = Field(widget=MapWidget(
        mapOptions={
            'scrollwheel': False,
        },
        latitudeSelector='div[class^="form-row"][class~="lat"]',
        longitudeSelector='div[class^="form-row"][class~="lon"]',
        ), required=False)

------------
Requirements
------------
- this fork use the jQuery.JSONParse method so jQuery >= 1.4.1 (Django 1.3 admin jQuery is ok)
