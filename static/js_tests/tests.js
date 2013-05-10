/* Unit tests for some of the functions we wrote that doesn't
 * involve Google Maps API.
 * */

test( "Meter Display Test", function() {
    var meter_info = {
        'congestion': 1,
        'enforcement_end': 6,
        'enforcement_start': 8,
        'key': 6715817022455808,
        'lat': 40.1079383377,
        'lon': -88.2291651578,
        'time_limit': 60,
        'time_per_quarter': 15,
    }
    meter_text = meterDisplay(meter_info);

    ok( meter_text == "60 minute parking<br>Meters enforced from 8AM to 6AM<br>$1.00 per hour<br>This meter is likely unoccupied<br>", "Passed!" );
});

test( "URL Encode Test", function() {
    encoded_string = "test%20string%20123%20_-%2B'";
    decoded_string = urldecode(encoded_string);

    ok( decoded_string == "test string 123 _-+'", "Passed!" );
});
