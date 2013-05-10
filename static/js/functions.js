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


// credit: http://jquery-howto.blogspot.com/2009/09/get-url-parameters-values-with-jquery.html
function getUrlVars() {
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for(var i = 0; i < hashes.length; i++) {
        hash = hashes[i].split('=');
        vars.push(hash[0]);
        vars[hash[0]] = hash[1];
    }
    return vars;
}


function urldecode(str) {
    return decodeURIComponent((str+'').replace(/\+/g, '%20'));
}


function calcRoute(directions, start, end, mode) {
    var travelmode;
    if (mode == "driving") {
        travelmode = google.maps.TravelMode.DRIVING;
        directions.setOptions({ polylineOptions: {strokeColor: "#00FF00"} });
    } else if (mode == "walking") {
        travelmode = google.maps.TravelMode.WALKING;
        directions.setOptions({
            polylineOptions: {
                strokeColor: "#000000",
            strokeWeight: 7,
            strokeOpacity: 0.8,
            zIndex: -4,
            } 
        });
    }

    var request = {
        origin:start,
        destination:end,
        travelMode: travelmode
    };
    directionsService.route(request, function(result, status) {
        if (status == google.maps.DirectionsStatus.OK) {
            directions.setOptions({ preserveViewport: true });
            directions.setDirections(result);
        }
    });
}


function resize() {
    $("#map-canvas").css("height",$(window).height()-$("#bottom").height());
}


function meterDisplay(meterData) {
    retString = "";
    var time_limit = parseInt(meterData.time_limit);
    if (time_limit > 60)
    {
        retString = retString + (Math.floor(time_limit / 60)).toString() + " hour parking<br>"; 
    }
    else
    {
        retString = retString + time_limit.toString() + " minute parking<br>";
    }

    var start = parseInt(meterData.enforcement_start);
    var end = parseInt(meterData.enforcement_end);

    if (start > 12)
    {
        start = (start - 12).toString() + "PM";
    }
    else if (start === 0)
    {
        start = "12AM";
    }
    else
    {
        start = start.toString() + "AM";
    }

    if (end > 12)
    {
        end = (end - 12).toString() + "PM";
    }
    else if (end === 0)
    {
        end = "12AM";
    }
    else
    {
        end = end.toString() + "AM";
    }
    retString = retString + "Meters enforced from " + start + " to " + end + "<br>";

    var tpq = parseInt(meterData.time_per_quarter);
    var cents = 100 * 15 / tpq % 100;
    if (cents < 10)
    {
        cents = cents.toString() + "0";
    }
    else
    {
        cents = cents.toString();
    }
    retString = retString + "$" + parseInt(15 / tpq).toString() + "." + cents + " per hour<br>";

    var con = parseInt(meterData.congestion);
    if (con < 4)
    {
        retString = retString + "This meter is likely unoccupied<br>";
    }
    if (con > 7)
    {
        retString = retString + "This meter is frequently occupied<br>";
    }
    return retString;
}
