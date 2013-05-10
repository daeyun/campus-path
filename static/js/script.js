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

    var destination_query = urldecode(getUrlVars().destination);

    var drivingDirections;
    var walkingDirections;
    var directionsService = new google.maps.DirectionsService();
    var locatingFrom, locatingTo;
    var map;


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
