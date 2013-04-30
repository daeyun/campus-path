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
    def get(self, routeID):
        template_values = {}
        template_values["route_id"] = routeID

        views = jinja_environment.get_template('route.html')
        self.response.out.write(views.render(template_values))


# /request
# GET -> new_request: Request
# Returns a list of routes not currently sorted by travel time.
class RequestRoutes(webapp2.RequestHandler):
    def get(self):
        new_request = self.request.get("new_request")

        #I'm going to use a temp value for now so we can discuss what my request will look like 

        place, (lat, lon) = geocode("700 E Green in Champaign")
        
        self.response.out.write(place)
        
        # query the data store and get the result
        result = ParkingMeter.proximity_fetch(
            ParkingMeter.query(),
            geo.geotypes.Point(lat, lon),
            max_results=10,
            max_distance=50000)

        print [p.to_dict() for p in result]




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


class GetMeters(webapp2.RequestHandler):
    def get(self):

        q = ndb.GqlQuery("SELECT * FROM ParkingMeters")
        result = q.fetch(1)

        self.response.out.write(result)


app = webapp2.WSGIApplication([
    ('/', MainView),
    ('/route/([0-9]+)', RouteView),
    ('/request', RequestRoutes),
    ('/submit', Submit),
    ('/meters', GetMeters),
    ('/setup', Initialize),
], debug=True)
