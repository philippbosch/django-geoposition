if (jQuery != undefined) {
    var django = {
        'jQuery':jQuery
    }
}

(function($) {
    
    window.geopositionMapInit = function() {
        var mapDefaults = {
            'mapTypeId': google.maps.MapTypeId.ROADMAP
        };
        
        $('p[data-map-widget]').each(function() {
            var $container = $(this),
                $mapContainer = $('<div class="geoposition-map"></div>'),
                $addressRow = $('<div class="geoposition-address"></div>'),
                $searchRow = $('<div class="geoposition-search"></div>'),
                $searchInput = $('<input>', {'type': 'search', 'placeholder': 'Search …'}),
                data = $.parseJSON($container.attr('data-map-widget')), //compatible with jQuery >= 1.4.1 (django >=1.3)
                $latitudeRow = $(data.latitudeSelector),
                $longitudeRow = $(data.longitudeSelector),
                $latitudeField = $($latitudeRow).find('input') || $latitudeRow,
                $longitudeField = $($longitudeRow).find('input') || $longitudeRow,
                latitude = parseFloat($latitudeField.val()) || 0,
                longitude = parseFloat($longitudeField.val()) || 0,
                map,
                mapLatLng,
                mapDefault = $.extend({}, mapDefaults, data.mapOptions),
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
                                var $ul = $('<ul></ul>', {'class': 'geoposition-results'});
                                $.each(results, function(i, result) {
                                    var $li = $('<li></li>');
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
            if (! $.contains($container.get(0), $latitudeRow.get(0))){
                $container.append($latitudeRow, $longitudeRow);
            }
            $container.append($mapContainer, $addressRow, $searchRow);
            
            mapLatLng = new google.maps.LatLng(latitude, longitude);
            mapOptions = $.extend({}, mapDefault, {
                'center': mapLatLng,
                'zoom': latitude || longitude ? 15 : 1
            });
            map = new google.maps.Map($mapContainer.get(0), mapOptions);
            marker = new google.maps.Marker({
                'position': mapLatLng,
                'map': map,
                'draggable': true,
                'animation': google.maps.Animation.DROP
            });
            var gc = new google.maps.Geocoder();
            var geocode = function(geocoder, marker){
                geocoder.geocode({
                    'latLng': marker.position
                }, function(results, status) {
                    $addressRow.text('');
                    if (results[0]) {
                        $addressRow.text(results[0].formatted_address);
                    }
                });
            };
            google.maps.event.addListener(marker, 'dragend', function() {
                $latitudeField.val(this.position.lat());
                $longitudeField.val(this.position.lng());
                geocode(gc, marker)
            });
            geocode(gc, marker);
        });
        
    };
    
    $(document).ready(function() {
        var $script = $('<script></script>');
        $script.attr('src', 'http://maps.google.com/maps/api/js?sensor=false&callback=geopositionMapInit');
        $script.appendTo('body');
    });
})(django.jQuery);
