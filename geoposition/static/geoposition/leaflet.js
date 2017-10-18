if (jQuery != undefined) {
    var django = {
        'jQuery': jQuery
    };
}


(function($) {

    $(document).ready(function() {

        try {
            var _ = L; // eslint-disable-line no-unused-vars
        } catch (ReferenceError) {
            console.log('geoposition: "L" not defined. You might not be connected to the internet.');
            return;
        }

        $('.geoposition-widget').each(function() {
            var $container = $(this),
                $mapContainer = $('<div class="geoposition-map" />'),
                $latitudeField = $container.find('input.geoposition:eq(0)'),
                $longitudeField = $container.find('input.geoposition:eq(1)'),
                latitude = parseFloat($latitudeField.val()) || null,
                longitude = parseFloat($longitudeField.val()) || null,
                map,
                marker;

            $mapContainer.css('height', $container.attr('data-map-widget-height') + 'px');

            function setLatLng(latLng) {
                $latitudeField.val(latLng.lat);
                $longitudeField.val(latLng.lng);
            }

            function getLatLng() {
                latitude = parseFloat($latitudeField.val()) || null;
                longitude = parseFloat($longitudeField.val()) || null;
                return {'lat': latitude, 'lng': longitude};
            }

            function mapClickListen(e) {
                setMarker(e.latlng);
            }

            function setMarker(latLng) {
                marker = L.marker(latLng, {draggable: true});
                marker.on('dragend', function(e) {
                    setLatLng(e.target.getLatLng());
                    map.panTo(e.target.getLatLng());
                });
                marker.addTo(map);
                map.panTo(latLng);
                setLatLng(latLng);
                // only one single marker allowed
                map.off('click', mapClickListen);
            }

            // create the map
            $container.append($mapContainer);
            map = L.map($mapContainer[0]).setView([51.505, -0.09], 13);
            L.tileLayer('https://{s}.tile.openstreetmap.de/tiles/osmde/{z}/{x}/{y}.png', {
                maxZoom: 18,
                attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            }).addTo(map);
            map.on('click', mapClickListen);

            // set marker if model has data already
            if ($latitudeField.val() && $longitudeField.val()) {
                setMarker(getLatLng());
                map.panTo(getLatLng(), {'animate': false});
            }

            // listen to keyboard input
            $latitudeField.add($longitudeField).bind('keyup', function() {
                var latLng = getLatLng();
                map.panTo(latLng);
                marker.setLatLng(latLng);
            });
        });
    });
})(django.jQuery);
