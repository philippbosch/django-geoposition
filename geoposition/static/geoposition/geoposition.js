(function($) {
    
    window.geopositionMapInit = function() {
        var mapDefaults = {
            'mapTypeId': google.maps.MapTypeId.ROADMAP
        };
        
        $('p.geoposition-widget').each(function() {
            var $container = $(this),
                $mapContainer = $('<div class="geoposition-map" />'),
                $addressRow = $('<div class="geoposition-address" />'),
                $latitudeField = $container.find('input.geoposition:eq(0)'),
                $longitudeField = $container.find('input.geoposition:eq(1)'),
                latitude = parseFloat($latitudeField.val()) || 0,
                longitude = parseFloat($longitudeField.val()) || 0,
                map,
                mapLatLng,
                mapOptions,
                marker;
            
            $container.append($mapContainer, $addressRow);
            
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
        $script.attr('src', 'http://maps.google.com/maps/api/js?sensor=false&callback=geopositionMapInit');
        $script.appendTo('body');
    });
})(django.jQuery);