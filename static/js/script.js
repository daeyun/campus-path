$(function() {


    // credit: http://jquery-howto.blogspot.com/2009/09/get-url-parameters-values-with-jquery.html
    function getUrlVars()
    {
        var vars = [], hash;
        var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
        for(var i = 0; i < hashes.length; i++)
        {
            hash = hashes[i].split('=');
            vars.push(hash[0]);
            vars[hash[0]] = hash[1];
        }
        return vars;
    }

    function urldecode(str) {
        return decodeURIComponent((str+'').replace(/\+/g, '%20'));
    }

    var destination_query = urldecode(getUrlVars().destination);

    var directionsDisplay;
    var directionsService = new google.maps.DirectionsService();
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
        directionsDisplay = new google.maps.DirectionsRenderer();
        var meters = (function () {
        var json = null;
        $.ajax({
            'async': false,
            'global': false,
            'url': '/request',
            'data' : {'new_request': destination_query},
            'dataType': "json",
            'success': function (data) {
            json = data;
            }
            });
        return json;
        })(); 

        $("span#location").html(meters.location_string);

        
        var mapOptions = {
            zoom: 15,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        var map = new google.maps.Map(document.getElementById('map-canvas'),
        mapOptions);
        directionsDisplay.setMap(map);

        var markers = [];

        /*
        lat = parseFloat(meters.location_lon);
        lon = parseFloat(meters.location_lat);
        latLng = new google.maps.LatLng(lon, lat);
        destination_marker = new google.maps.Marker({
            position: latLng,
            draggable: false,
            map: map,
            icon:'http://maps.google.com/mapfiles/ms/icons/green-dot.png'
        });
        */
        var infowindow_content = '';
        var infowindow = new google.maps.InfoWindow({
        });

        for (var i = 0; i < meters.meters.length; ++i) {
            lat = meters.meters[i].lat
            lon = meters.meters[i].lon
            var latLng = new google.maps.LatLng(lat, lon);
            var marker = new google.maps.Marker({
                position: latLng,
                draggable: false,
                data: meters.meters[i],
            });
            google.maps.event.addListener(marker, 'click', function(){
                infowindow.setContent(
                    this.data.lat.toString() + "," +
                    this.data.lon.toString() + "<br />" +
                    this.data.congestion.toString()
                    );
                infowindow.open(map,this);
            });

            markers.push(marker);

        }

        var mcOptions = {gridSize: 30, maxZoom: 17};
        markerClusterer = new MarkerClusterer(map, markers, mcOptions);


        var current_lat, current_lon;
        // Try HTML5 geolocation
        if(navigator.geolocation) {
            console.log("geolocation works");
            navigator.geolocation.getCurrentPosition(function(position) {
                var current_pos = new google.maps.LatLng(position.coords.latitude,
                position.coords.longitude);

                calcRoute(current_pos);

                var infowindow = new google.maps.InfoWindow({
                    map: map,
                    position: current_pos,
                    content: 'Location found using HTML5.'
                });

                map.setCenter(current_pos);
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

    function calcRoute(pos) {
        console.log(pos);
        var start = pos;
        var request = {
            origin:start,
            destination:destination_query,
            travelMode: google.maps.TravelMode.DRIVING
        };
        console.log(destination_query);
        directionsService.route(request, function(result, status) {
            if (status == google.maps.DirectionsStatus.OK) {
            directionsDisplay.setDirections(result);
            }
        });
    }
    
    function resize() {
        $("#map-canvas").css("height",$(window).height()-50);
    }
    resize();

    $(window).resize(function() {
        resize();
    });
    
    //Example used from google's direction API

   /* $.getJSON('/static/data/meters.json', function(data) {
        initialize(data)
    })
    .done(function() { console.log( "second success" ); })
    .fail(function() { console.log( "error" ); })
    .always(function() { console.log( "complete" ); });*/

});
