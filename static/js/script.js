$(function() {
    $('#myModal form').on('submit', function(event) {
        var $form = $(this);
        $.ajax({
            type: $form.attr('method'),
            url: $form.attr('action'),
            data: $form.serialize(),

            success: function(data, status) {
                if (data == "ok") {
                    $('#myModal').modal('hide');
                }
            }
        });

        event.preventDefault();
    });


    var drivingDirections;
    var walkingDirections;
    var directionsService = new google.maps.DirectionsService();
    var locatingFrom, locatingTo;
    var map;
    var destination_query = urldecode(getUrlVars().destination);

    function initialize() {
        /*
           the following code is largely from a google api example
           Include the maps javascript with sensor=true because this code is using a
           sensor (a GPS locator) to determine the user's location.
           See: https://developers.google.com/apis/maps/documentation/javascript/basics#SpecifyingSensor
           */
        console.log("running initialize function");
        drivingDirections = new google.maps.DirectionsRenderer();
        walkingDirections = new google.maps.DirectionsRenderer();
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

        var infowindow = new google.maps.InfoWindow(); 

        var current_lat, current_lon;
        if(navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {

                $("#loading").hide(0);
                $("#bottom").show();

                var current_pos = new google.maps.LatLng(position.coords.latitude,
                    position.coords.longitude);

                var mapOptions = {
                    zoom: 15,
                mapTypeId: google.maps.MapTypeId.ROADMAP
                };
                var map = new google.maps.Map(document.getElementById('map-canvas'),
                    mapOptions);
                drivingDirections.setMap(map);
                walkingDirections.setMap(map);

                var markers = [];

                lat = parseFloat(meters.location_lon);
                lon = parseFloat(meters.location_lat);
                var queryLatLng = new google.maps.LatLng(lon, lat);
                destination_marker = new google.maps.Marker({
                    position: queryLatLng,
                                   draggable: false,
                                   optimized: false,
                                   map: map,
                                   zIndex:10,
                                   icon:'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
                });

                for (var i = 0; i < meters.meters.length; ++i) {
                    lat = meters.meters[i].lat;
                    lon = meters.meters[i].lon;
                    var latLng = new google.maps.LatLng(lat, lon);
                    var marker = new google.maps.Marker({
                        position: latLng,
                        draggable: false,
                        optimized: false,
                        data: meters.meters[i],
                    });
                    google.maps.event.addListener(marker, 'click', function(){
                        infowindow.setContent(
                            meterDisplay(this.data) +
                            '<br /><button class="btn" id="updateBtn" type="button">Update</button>'
                            );

                        $("#myModal #key").val(this.data.key.toString());
                        $("#myModal #congestion").val(this.data.congestion.toString());
                        $("#myModal #time_limit").val(this.data.time_limit.toString());
                        $("#myModal #time_per_quarter").val(this.data.time_per_quarter.toString());
                        $("#myModal #enforcement_start").val(this.data.enforcement_start.toString());
                        $("#myModal #enforcement_end").val(this.data.enforcement_end.toString());

                        infowindow.open(map,this);

                        meter_pos = new google.maps.LatLng(this.data.lat.toString(),
                            this.data.lon.toString());
                        calcRoute(drivingDirections, current_pos, meter_pos, "driving");
                        calcRoute(walkingDirections, meter_pos, destination_query, "walking");

                    });
                    markers.push(marker);
                }
                var mcOptions = {gridSize: 30, maxZoom: 17};
                markerClusterer = new MarkerClusterer(map, markers, mcOptions);

                var infowindow = new google.maps.InfoWindow({
                    map: map,
                    position: current_pos,
                    content: 'Current Location'
                });

                map.setCenter(queryLatLng);

            }, function() {
                handleNoGeolocation(true);
            });
        } else {
            // Browser doesn't support Geolocation
            console.log("geolocation does not work");
            handleNoGeolocation(false);
        }
    }

    $(document).on( "click", "#updateBtn", function(){
        $('#myModal').modal('show');
    } );

    google.maps.event.addDomListener(window, 'load', initialize);

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

    resize();

    $(window).resize(function() {
        resize();
    });
});
