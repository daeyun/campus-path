import webapp2, os, jinja2, json, datetime
from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext import ndb
from geocode import *
from models import *
import sys
import csv

import json

from geo.geomodel import GeoModel


def makeMeterDict(meter):
    meter_dict={}
    meter_dict['key'] = meter.key.id()
    meter_dict['lat'] = meter._get_latitude()
    meter_dict['lon'] = meter._get_longitude()
    meter_dict['time_limit'] = meter.time_limit
    meter_dict['time_per_quarter'] = meter.time_per_quarter
    meter_dict['enforcement_start'] = meter.enforcement_start
    meter_dict['enforcement_end'] = meter.enforcement_end
    meter_dict['congestion'] = meter.congestion
    return meter_dict

def populate():
    finput = csv.reader(open("data/parkingmeters.csv", 'rb'),
                        delimiter=',', quotechar='"')
    finput = list(finput)
    
    locations = []
    for row in finput[1:]:
        row = row[0].split(",")
        lat = row[0][1:]
        lon = row[1][:-1]
        parking_meter = ParkingMeter(location=ndb.GeoPt(float(lat), float(lon)),
                                     time_limit=60,
                                     time_per_quarter=15,
                                     enforcement_start=8,
                                     enforcement_end=6,
                                     congestion=1)
            
        parking_meter.update_location()
        parking_meter.put()


    return str(lat) + " " + str(lon)


