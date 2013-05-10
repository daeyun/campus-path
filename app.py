import webapp2, os, jinja2, json, datetime, random, hashlib
from google.appengine.api import users
from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template
from models import *
from helpers import *
import geo.geotypes

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(
    os.path.join(os.path.dirname(__file__), 'templates/')),
    comment_start_string='{!')


class MainView(webapp2.RequestHandler):
    def get(self):
        template_values = {}

        views = jinja_environment.get_template('main.html')
        self.response.out.write(views.render(template_values))


class RouteView(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        template_values["destination"] = self.request.get("destination")

        views = jinja_environment.get_template('route.html')
        self.response.out.write(views.render(template_values))


# /request
# GET -> new_request: Request
# Returns a list of routes not currently sorted by travel time.
class RequestMeters(webapp2.RequestHandler):
    def get(self):
        request_string = self.request.get("new_request", default_value="")
        if request_string == "":
            return

        place, (lat, lon) = geocode(request_string)

        #see if we've cached this
        json_response = memcache.get(place)
        if json_response is not None:
            self.response.out.write(json_response)
            return

        
        # query the data store and get the result
        result = ParkingMeter.proximity_fetch(
            ParkingMeter.query(),
            geo.geotypes.Point(lat, lon),
            max_results=200,
            max_distance=50000)

        meters = []

        #if someone wants to make this non-ugly, please go ahead
        print meter
        for meter in result:
            meters.append(makeMeterDict(meter))

        return_dict = {}
        return_dict['location_string'] = place
        return_dict['location_lat'] = lat
        return_dict['location_lon'] = lon
        return_dict['meters'] = meters

        json_response = json.dumps(return_dict)
        memcache.add(place, json_response)
        self.response.out.write(json_response)
            


class Initialize(webapp2.RequestHandler):
    def get(self):
        command = self.request.get("command")

        status = "ok"
        if command == "populate":
            status = populate()

        self.response.out.write(status)


class Update(webapp2.RequestHandler):
    def post(self):
        key = self.request.get("key")
        # lat = self.request.get("lat")
        # lon = self.request.get("lon")
        tl = int(self.request.get("time_limit"))
        tpq = int(self.request.get("time_per_quarter"))
        es = int(self.request.get("enforcement_start"))
        ee = int(self.request.get("enforcement_end"))
        con = int(self.request.get("congestion"))


        if (tl > 600) or (tl < 1):
            status = "Input Error: Time limit range"
            self.response.out.write(status)
            return

        if (con > 10) or (con < 0):
            status = "Input Error: Congestion range"
            self.response.out.write(status)
            return

        '''
        #new meters should pass "new" for the key
        #this is not currently implemented
        if key == "new":
            meter = ParkingMeter(location=ndb.GeoPt(float(lat), float(lon)),
                                 time_limit=tl,
                                 time_per_quarter=tpq,
                                 enforcement_start=es,
                                 enforcement_end=ee,
                                 congestion=con)
            meter.update_location()
        else:
        '''
            #assuming non-new meters don't move (ignoring lat/lon)
        meter_key = ndb.Key(ParkingMeter, int(key))
        meter = meter_key.get()
        meter.time_limit=tl
        meter.time_per_quarter=tpq
        meter.enforcement_start=es
        meter.enforcement_end=ee
        meter.congestion=con

        #be sure to stay consistent in memcache
        #this can likely be made finer-grained at some point
        memcache.flush_all()

        meter.put()

        status = "ok"
        self.response.out.write(status)


app = webapp2.WSGIApplication([
    ('/', MainView),
    ('/route', RouteView),
    ('/request', RequestMeters),
    ('/update', Update),
    ('/setup', Initialize),
], debug=True)
