import webapp2, os, jinja2, json, datetime
from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext import ndb

from geo.geomodel import GeoModel

class ParkingMeter(GeoModel, ndb.Model):
    time_limit = ndb.IntegerProperty()     #in minutes
    time_per_quarter = ndb.IntegerProperty()     #in minutes per quarter
    enforcement_start = ndb.IntegerProperty()    #in 24h times
    enforcement_end = ndb.IntegerProperty()    #in 24h times
    congestion = ndb.IntegerProperty()    #on a scale of 1-10


    #the following methods are borrowed (and modified) from the publicschools geomodel example 

    @staticmethod
    def public_attributes():
        """Returns a set of simple attributes on parking meter entities."""
        return [
            'time_limit', 'time_per_quarter', 'enforcement_start', 'enforcement_end', 'congestion'
            ]

    def _get_latitude(self):
        return self.location.lat if self.location else None

    def _set_latitude(self, lat):
        if not self.location:
            self.location = ndb.GeoPt()

        self.location.lat = lat

    latitude = property(_get_latitude, _set_latitude)

    def _get_longitude(self):
        return self.location.lon if self.location else None

    def _set_longitude(self, lon):
        if not self.location:
            self.location = ndb.GeoPt()

        self.location.lon = lon

    longitude = property(_get_longitude, _set_longitude)
