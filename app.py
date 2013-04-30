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
        request_string = self.request.get("new_request")

        #I'm going to use a temp value for now so we can discuss what my request will look like 

        place, (lat, lon) = geocode(request_string)
        
#        self.response.out.write(place)
        
        # query the data store and get the result
        result = ParkingMeter.proximity_fetch(
            ParkingMeter.query(),
            geo.geotypes.Point(lat, lon),
            max_results=50,
            max_distance=50000)

        meters = []

        #if someone wants to make this non-ugly, please go ahead
        for meter in result:
            meters.append(makeMeterDict(meter))

        return_dict = {}
        return_dict['location_string'] = place
        return_dict['location_lat'] = lat
        return_dict['location_lon'] = lon
        return_dict['meters'] = meters
        
        self.response.out.write(json.dumps(return_dict))
            


# /submit
# POST -> route: Route, start_time: time, end_time: time
# Submits a feedback on how long it actually took. Start and end times are
# kept on the client side.
class Submit(webapp2.RequestHandler):
    def post(self):
        route = self.request.get("route")
        start_time = self.request.get("start_time")
        end_time = self.request.get("end_time")

        # submit and return the status

        status = "ok"
        self.response.out.write(status)


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
        lat = self.request.get("lat")
        lon = self.request.get("lon")
        time_limit = self.request.get("time_limit")
        time_per_quarter = self.request.get("time_per_quarter")
        enforcement_start = self.request.get("enforcement_start")
        enforcement_end = self.request.get("enforcement_end")
        congestion = self.request.get("congestion")
        

app = webapp2.WSGIApplication([
    ('/', MainView),
    ('/route', RouteView),
    ('/request', RequestMeters),
    ('/submit', Submit),
    ('/update', Update),
    ('/setup', Initialize),
], debug=True)
