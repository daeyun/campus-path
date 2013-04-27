$(function() {


    var locatingFrom, locatingTo;
    var map;

    // <!-- the following code is largely from a google api example -->
    // <!--
    // Include the maps javascript with sensor=true because this code is using a
    // sensor (a GPS locator) to determine the user's location.
    // See: https://developers.google.com/apis/maps/documentation/javascript/basics#SpecifyingSensor
    // -->
    // <!-- end google api example -->
    function initialize() {
        console.log("running initialize function");

        var meters = (function () {
        var json = null;
        $.ajax({
            'async': false,
            'global': false,
            'url': '/static/data/meters.json',
            'dataType': "json",
            'success': function (data) {
            json = data;
            }
            });
        return json;
        })(); 
        
        var mapOptions = {
            zoom: 15,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        var map = new google.maps.Map(document.getElementById('map-canvas'),
        mapOptions);

        var markers = [];

        for (var i = 0; i < meters.length; ++i) {
            l = meters.data[i].split(', ')
            var latLng = new google.maps.LatLng(l[0], l[1]);
            var marker = new google.maps.Marker({
                position: latLng,
                draggable: false,
            });
            markers.push(marker);

        }
            var mcOptions = {gridSize: 50, maxZoom: 15};
            markerClusterer = new MarkerClusterer(map, markers);

        // Try HTML5 geolocation
        if(navigator.geolocation) {
            console.log("geolocation works");
            navigator.geolocation.getCurrentPosition(function(position) {
                var pos = new google.maps.LatLng(position.coords.latitude,
                position.coords.longitude);

                var infowindow = new google.maps.InfoWindow({
                    map: map,
                    position: pos,
                    content: 'Location found using HTML5.'
                });

                map.setCenter(pos);
                }, function() {
                handleNoGeolocation(true);
            });
            } else {
            // Browser doesn't support Geolocation
            handleNoGeolocation(false);
        }
        }
    
    google.maps.event.addDomListener(window, 'load', initialize);

    function handleNoGeolocation(errorFlag) {
        if (errorFlag) {
            var content = 'Error: The Geolocation service failed.';
        } else {
            var content = 'Error: Your browser doesn\'t support geolocation.';
        }

        var options = {
            map: map,
            position: new google.maps.LatLng(60, 105),
            content: content
        };

        var infowindow = new google.maps.InfoWindow(options);
        map.setCenter(options.position);
    }

    $("a.locateFrom").click(function(e){
        e.preventDefault();
        locatingFrom = true;
    });

    $("a.locateTo").click(function(e){
        e.preventDefault();
        locatingTo = true;
    });

    $("a.locateFrom, a.locateTo").click(function(e){
        e.preventDefault();
        $("#map-window").show();
        initialize();
        google.maps.event.addListener(map, "click", function(event) {
            var lat = event.latLng.lat();
            var lng = event.latLng.lng();
            if (locatingFrom)
                $("#inputFrom").val(lat + ", " + lng);
            else if (locatingTo)
                $("#inputTo").val(lat + ", " + lng);
            locatingFrom = false;
            locatingTo = false;
            $("#map-window").hide();
        });

    });

   /* $.getJSON('/static/data/meters.json', function(data) {
        initialize(data)
    })
    .done(function() { console.log( "second success" ); })
    .fail(function() { console.log( "error" ); })
    .always(function() { console.log( "complete" ); });*/

});
