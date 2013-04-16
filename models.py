import webapp2, os, jinja2, json, datetime
from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext import ndb


class RouteUnit(ndb.Model):
    transportation = ndb.StringProperty()
    start = ndb.GeoPtProperty()
    end = ndb.GeoPtProperty()
    duration = ndb.IntegerProperty()
    date = ndb.DateTimeProperty()
