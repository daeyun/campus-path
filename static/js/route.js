$(function(){
console.log("running script _at all_");
var map;
   
    function initialize(data) {
        console.log("running initialize function");

        var mapOptions = {
          zoom: 6,
          mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        map = new google.maps.Map(document.getElementById('map-canvas'),
            mapOptions);
        var raw;
        var markers = [];
       
        
        for (var i = 0; i < 100; ++i) {
          console.log(raw.data[i]);
        }
        for (var i = 0; i < 100; ++i) {
          var latLng = new google.maps.LatLng(raw.data[i], raw.data[i].longitude);
          var marker = new google.maps.Marker({
            position: latLng,
            draggable: false,
          });
          markers.push(marker);

        var mcOptions = {gridSize: 50, maxZoom: 15};
        markerClusterer = new MarkerClusterer(map, markers, mcOptions);


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

      function handleNoGeolocation(errorFlag) {
        if (errorFlag) {
          var content = 'Error: The Geolocation service failed.';
        } 
        else {
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
      }
      $.getJSON('/static/js/raw.json', function(data){
      initialize(data)
     // alert(JSON.property);
      });
      google.maps.event.addDomListener(window, 'load', initialize);
});