if (jQuery != undefined) {
    var django = {
        'jQuery': jQuery,
    }
}

(function($) {
    $(document).ready(function() {

        try {
            var _ = google;
        } catch (ReferenceError) {
            console.log('geoposition: "google" not defined.  You might not be connected to the internet.');
            return;
        }

        var mapDefaults = {
            'mapTypeId': google.maps.MapTypeId.ROADMAP,
            'scrollwheel': true,
            'streetViewControl': false,
            'panControl': true
        };

        var markerDefaults = {
            'draggable': true,
            'animation': google.maps.Animation.DROP
        };

        $('.geoposition-widget').each(function() {
            var $container = $(this),
                $mapWrapper = $('<div class="geoposition-map-wrapper"/>'),
                $mapContainer = $('<div class="geoposition-map"/>'),
                $addressRow = $('<div class="geoposition-address"/>'),
                $searchInput = $('<input>', {
                    'type': 'search',
                    'placeholder': 'Start typing an address …'
                }),
                $latitudeField = $container.find('input.geoposition:eq(0)'),
                $longitudeField = $container.find('input.geoposition:eq(1)'),
                $elevationField = $container.find('input.geoposition:eq(2)'),
                latitude = parseFloat($latitudeField.val()) || null,
                longitude = parseFloat($longitudeField.val()) || null,
                elevation = parseFloat($elevationField.val()) || null,
                map,
                mapLatLng,
                mapOptions,
                mapCustomOptions,
                markerOptions,
                markerCustomOptions,
                marker;

            $mapContainer.css('height', $container.data('map-widget-height') + 'px');
            mapCustomOptions = $container.data('map-options') || {};
            markerCustomOptions = $container.data('marker-options') || {};

            function doSearch() {
                var gc = new google.maps.Geocoder();
                $searchInput.parent().find('ul.geoposition-results').remove();
                gc.geocode({
                    'address': $searchInput.val()
                }, function(results, status) {
                    if (status == 'OK') {
                        var updatePosition = function(result) {
                            if (result.geometry.bounds) {
                                map.fitBounds(result.geometry.bounds);
                            } else {
                                map.panTo(result.geometry.location);
                                map.setZoom(18);
                            }
                            marker.setPosition(result.geometry.location);
                            google.maps.event.trigger(marker, 'dragend');
                        };
                        if (results.length == 1) {
                            updatePosition(results[0]);
                        } else {
                            var $ul = $('<ul />', {
                                'class': 'geoposition-results'
                            });
                            $.each(results, function(i, result) {
                                var $li = $('<li />');
                                $li.text(result.formatted_address);
                                $li.on('click', function() {
                                    updatePosition(result);
                                    $li.closest('ul').remove();
                                });
                                $li.appendTo($ul);
                            });
                            $searchInput.after($ul);
                        }
                    }
                });
            }

            function doGeocode() {
                var gc = new google.maps.Geocoder();
                gc.geocode({
                    'latLng': marker.position
                }, function(results, status) {
                    $addressRow.text('');
                    if (results && results[0]) {
                        $addressRow.text(results[0].formatted_address);
                    }
                });
            }

            var autoSuggestTimer = null;
            $searchInput.on('keydown', function(e) {
                if (autoSuggestTimer) {
                    clearTimeout(autoSuggestTimer);
                    autoSuggestTimer = null;
                }

                // if enter, search immediately
                if (e.keyCode == 13) {
                    e.preventDefault();
                    doSearch();
                } else {
                    // otherwise, search after a while after typing ends
                    autoSuggestTimer = setTimeout(function() {
                        doSearch();
                    }, 1000);
                }
            }).on('abort', function() {
                $(this).parent().find('ul.geoposition-results').remove();
            });
            $searchInput.appendTo($mapWrapper);
            $addressRow.appendTo($mapWrapper);
            $mapContainer.appendTo($mapWrapper);

            $container.append($mapWrapper);

            mapLatLng = new google.maps.LatLng(latitude, longitude);

            mapOptions = $.extend({}, mapDefaults, mapCustomOptions);

            if (!(latitude === null && longitude === null && mapOptions['center'])) {
                mapOptions['center'] = mapLatLng;
            }

            if (!mapOptions['zoom']) {
                mapOptions['zoom'] = latitude && longitude ? 15 : 1;
            }

            map = new google.maps.Map($mapContainer.get(0), mapOptions);
            markerOptions = $.extend({}, markerDefaults, markerCustomOptions, {
                'map': map
            });

            if (!(latitude === null && longitude === null && markerOptions['position'])) {
                markerOptions['position'] = mapLatLng;
            }

            marker = new google.maps.Marker(markerOptions);
            var elevator = new google.maps.ElevationService;

            google.maps.event.addListener(marker, 'dragend', function() {
                $latitudeField.val(this.position.lat());
                $longitudeField.val(this.position.lng());

                elevator.getElevationForLocations({
                    'locations':[{
                        lat: this.position.lat(),
                        lng: this.position.lng()
                    }]
                }, function(response, status){
                    var elevation = 0.0;
                    if(status==='OK'){
                        elevation = response[0].elevation;
                    }
                    $elevationField.val(elevation);
                });

                doGeocode();
            });

            if ($latitudeField.val() && $longitudeField.val()) {
                google.maps.event.trigger(marker, 'dragend');
            }

            $latitudeField.add($longitudeField).on('keyup', function(e) {
                var latitude = parseFloat($latitudeField.val()) || 0;
                var longitude = parseFloat($longitudeField.val()) || 0;
                var center = new google.maps.LatLng(latitude, longitude);
                map.setCenter(center);
                map.setZoom(15);
                marker.setPosition(center);
                doGeocode();
            });
        });
    });
})(django.jQuery);
