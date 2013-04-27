import webapp2, os, jinja2, json, datetime
from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext import ndb
from models import *
import sys
import csv


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
            locations.append(lat+','+lon)

        print locations
        p = ParkingMeters(locations=locations)
        k = p.put()
        print k

    except IOError as (errno, strerror):
            print "I/O error({0}): {1}".format(errno, strerror)
    except:
            print "Unexpected Error: ", sys.exc_info()[0]
            raise

    return
