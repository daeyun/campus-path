import webapp2, os, jinja2, json, datetime
from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext import ndb

from geo.geomodel import GeoModel

class ParkingMeter(GeoModel):
    #in minutes
    time_limit = ndb.IntegerProperty()

    #in minutes per quarter
    time_per_quarter = ndb.IntegerProperty()

    #in 24h times
    enforcement_start = ndb.IntegerProperty()

    #in 24h times
    enforcement_end = ndb.IntegerProperty()

    #on a scale of 1-10
    congestion = ndb.IntegerProperty()

    @staticmethod
    def public_attributes():
        """Returns a set of simple attributes on public school entities."""
        return [
            'time_limit', 'time_per_quarter', 'enforcement_start', 'enforcement_end', 'congestion'
            ]

    def _get_latitude(self):
        return self.location.lat if self.location else None

    def _set_latitude(self, lat):
        if not self.location:
            self.location = db.GeoPt()

        self.location.lat = lat

    latitude = property(_get_latitude, _set_latitude)

    def _get_longitude(self):
        return self.location.lon if self.location else None

    def _set_longitude(self, lon):
        if not self.location:
            self.location = db.GeoPt()

        self.location.lon = lon

    longitude = property(_get_longitude, _set_longitude)
