if (jQuery != undefined) {
    var django = {
        'jQuery':jQuery,
    }
}
(function($) {

    window.geopositionMapInit = function() {
        var mapDefaults = {
            'mapTypeId': google.maps.MapTypeId.ROADMAP,
            'scrollwheel': false
        };

        $('p.geoposition-widget').each(function() {
            var $container = $(this),
                $mapContainer = $('<div class="geoposition-map" />'),
                $addressRow = $('<div class="geoposition-address" />'),
                $searchRow = $('<div class="geoposition-search" />'),
                $searchInput = $('<input>', {'type': 'search', 'placeholder': 'Search …'}),
                $latitudeField = $container.find('input.geoposition:eq(0)'),
                $longitudeField = $container.find('input.geoposition:eq(1)'),
                latitude = parseFloat($latitudeField.val()) || 0,
                longitude = parseFloat($longitudeField.val()) || 0,
                map,
                mapLatLng,
                mapOptions,
                marker;


            $searchInput.bind('keydown', function(e) {
                if (e.keyCode == 13) {
                    e.preventDefault();
                    var $input = $(this),
                        gc = new google.maps.Geocoder();
                    $input.parent().find('ul.geoposition-results').remove();
                    gc.geocode({
                        'address': $(this).val()
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
                                var $ul = $('<ul />', {'class': 'geoposition-results'});
                                $.each(results, function(i, result) {
                                    var $li = $('<li />');
                                    $li.text(result.formatted_address);
                                    $li.bind('click', function() {
                                        updatePosition(result);
                                        $li.closest('ul').remove();
                                    });
                                    $li.appendTo($ul);
                                });
                                $input.after($ul);
                            }
                        }
                    });
                }
            }).bind('abort', function() {
                $(this).parent().find('ul.geoposition-results').remove();
            });
            $searchInput.appendTo($searchRow);
            $container.append($mapContainer, $addressRow, $searchRow);

            mapLatLng = new google.maps.LatLng(latitude, longitude);
            mapOptions = $.extend({}, mapDefaults, {
                'center': mapLatLng,
                'zoom': latitude && longitude ? 15 : 1
            });
            map = new google.maps.Map($mapContainer.get(0), mapOptions);
            marker = new google.maps.Marker({
                'position': mapLatLng,
                'map': map,
                'draggable': true,
                'animation': google.maps.Animation.DROP
            });
            google.maps.event.addListener(marker, 'dragend', function() {
                $latitudeField.val(this.position.lat());
                $longitudeField.val(this.position.lng());

                var gc = new google.maps.Geocoder();
                gc.geocode({
                    'latLng': marker.position
                }, function(results, status) {
                    $addressRow.text('');
                    if (results[0]) {
                        $addressRow.text(results[0].formatted_address);
                    }
                });
            });
            google.maps.event.trigger(marker, 'dragend');
        });

    };

    $(document).ready(function() {
        var $script = $('<script/>');
        $script.attr('src', 'https://maps.google.com/maps/api/js?sensor=false&callback=geopositionMapInit');
        $script.appendTo('body');
    });
})(django.jQuery);
