import json

from urllib import urlencode
from urllib2 import urlopen

#get_encoding, decode_page, check_status, and geocode are largely 
#from the GoogleV3 module in the geopy library

def get_encoding(page, contents=None):
    charset = page.headers.getparam("charset") or None

    if charset:
        return charset

    if contents:
        try:
            return xml.dom.minidom.parseString(contents).encoding
        except ExpatError:
            pass

def decode_page(page):
    contents = page.read()
    # HTTP 1.1 defines iso-8859-1 as the 'implied' encoding if none is given
    encoding = get_encoding(page, contents) or 'iso-8859-1'
    return unicode(contents, encoding=encoding).encode('utf-8')


def check_status(status):
    '''Validates error statuses.'''
    if status == 'ZERO_RESULTS':
        raise GQueryError(
            'The geocode was successful but returned no results. This may'
            ' occur if the geocode was passed a non-existent address or a'
            ' latlng in a remote location.')
    elif status == 'OVER_QUERY_LIMIT':
        raise GTooManyQueriesError(
            'The given key has gone over the requests limit in the 24'
            ' hour period or has submitted too many requests in too'
            ' short a period of time.')
    elif status == 'REQUEST_DENIED':
        raise GQueryError(
            'Your request was denied, probably because of lack of a'
            ' sensor parameter.')
    elif status == 'INVALID_REQUEST':
        raise GQueryError('Probably missing address or latlng.')
    else:
        raise GeocoderResultError('Unkown error.')

def geocode(string):
    if isinstance(string, unicode):
        string = string.encode('utf-8')

    params = { 
        'address': string,
        'sensor': str(False).lower()
        }
        
    page = urlopen('http://maps.googleapis.com/maps/api/geocode/json?%(params)s' % ({'params': urlencode(params)}))

    if not isinstance(page, basestring):
        page = decode_page(page)
    doc = json.loads(page)
    places = doc.get('results', [])

    if not places:
        check_status(doc.get('status'))
    elif len(places) != 1:
        raise ValueError(
            "Didn't find exactly one placemark! (Found %d)" % len(places))

    def parse_place(place):
        '''Get the location, lat, lng from a single json place.'''
        location = place.get('formatted_address')
        latitude = place['geometry']['location']['lat']
        longitude = place['geometry']['location']['lng']
        return (location, (latitude, longitude))

    return parse_place(places[0])

