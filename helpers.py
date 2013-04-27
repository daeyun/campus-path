import webapp2, os, jinja2, json, datetime
from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext import ndb
from models import *
import sys
import csv

from geo.geomodel import GeoModel


def populate():
    try:
        finput = csv.reader(open("data/parkingmeters.csv", 'rb'),
                            delimiter=',', quotechar='"')
        finput = list(finput)

        locations = []
        for row in finput[1:]:
            row = row[0].split(",")
            lat = row[0][1:]
            lon = row[1][:-1]
            parking_meter = ParkingMeter(location=ndb.GeoPt(lat, lon), 
                                         time_limit=60,
                                         time_per_quarter=15,
                                         enforcement_start=8,
                                         enforcement_end=6,
                                         congestion=1)
            parking_meter.put()


    except IOError as (errno, strerror):
            print "I/O error({0}): {1}".format(errno, strerror)
    except:
            print "Unexpected Error: ", sys.exc_info()[0]
            raise

    return
