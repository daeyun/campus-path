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
