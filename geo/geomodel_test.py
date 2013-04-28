#!/usr/bin/python2.5
#
# Copyright 2009 Roman Nurik
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Unit tests for geomodel.py."""

import os
import sys
# Hardcoded Path to SDK.
gae_path = '/usr/local/google_appengine'
sys.path[0:0] = [
    # Minimum SDK libs required.
    gae_path,
    os.path.join(gae_path, 'lib', 'yaml', 'lib'),
]

import unittest

from google.appengine.ext import ndb
from google.appengine.ext import testbed

import geomodel
import geotypes


# Borrowed from the demo.
class PublicSchool(geomodel.GeoModel, ndb.Model):
  """A location-aware model for public school entities.

  See http://nces.ed.gov/ccd/psadd.asp for details on attributes.
  """
  school_id = ndb.StringProperty()
  name = ndb.StringProperty()
  address = ndb.StringProperty()
  city = ndb.StringProperty()
  state = ndb.StringProperty()
  zip_code = ndb.IntegerProperty()
  enrollment = ndb.IntegerProperty()
  phone_number = ndb.StringProperty()
  locale_code = ndb.IntegerProperty()
  school_type = ndb.IntegerProperty()
  school_level = ndb.IntegerProperty()
  grades_taught = ndb.IntegerProperty(repeated=True)

  @staticmethod
  def public_attributes():
    """Returns a set of simple attributes on public school entities."""
    return [
      'school_id', 'name', 'address', 'city', 'state', 'zip_code',
      'enrollment', 'phone_number', 'locale_code', 'school_type', 'school_level'
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


class AppTest(unittest.TestCase):
  """Base class for tests that use App Engine services."""

  APP_ID = '_'

  def setUp(self):
    self.testbed = testbed.Testbed()
    self.testbed.setup_env(app_id=self.APP_ID)
    self.testbed.activate()
    self.testbed.init_datastore_v3_stub()
    self.testbed.init_memcache_stub()

  def tearDown(self):
    self.testbed.deactivate()


def _populate_db():
  data = """390000104683,OHIO SCHOOL FOR THE DEAF,500 MORSE RD,COLUMBUS,OH,43214,1833,18,(614) 728-1424,11,2,2,06,08,1,40.064882,-83.004279,9
390000204684,STATE SCHOOL FOR THE BLIND,5220 N HIGH ST,COLUMBUS,OH,43214,1240,80,(614) 752-1359,11,2,3,07,12,1,40.069993,-83.007824,9
390001701509,YOUNGSTOWN COMMUNITY SCHOOL,50 ESSEX ST,YOUNGSTOWN,OH,44502,1838,321,(330) 746-2240,13,1,1,KG,06,1,41.090543,-80.658638,9
390001801513,EAGLE HEIGHTS ACADEMY,1833 MARKET ST,YOUNGSTOWN,OH,44507,1137,719,(330) 742-9090,13,1,1,KG,08,1,41.081567,-80.655892,9
390001901514,CONSTELLATION SCHOOLS: OLD BROOKLYN COMMUNITY ELEM,4430 STATE RD,CLEVELAND,OH,44109,4705,274,(216) 661-7888,11,1,1,KG,04,1,41.433879,-81.707919,9
390002001515,HARMONY COMMUNITY SCHOOL,1580 SUMMIT RD,CINCINNATI,OH,45237,1917,-2,(513) 921-5260,11,1,N,07,12,2,39.20326,-84.464114,9
590010500138,SHERMAN INDIAN HIGH SCHOOL,9010 MAGNOLIA AVE,RIVERSIDE,CA,92503,,330,(951) 276-6326,N,1,3,09,12,1,33.925504,-117.437367,9
590019700136,NOLI SCHOOL,PO BOX 700,SAN JACINTO,CA,92581,,129,(951) 654-5596,N,1,4,06,12,1,33.784426,-116.958389,9"""

  props = ['school_id', 'name', 'address', 'city', 'state', 'zip_code',
    '_dummy', 'enrollment', 'phone_number', 'locale_code', 'school_type',
    'school_level', '_dummy', '_dummy', '_dummy', 'lat', 'lon',
    'accuracy']

  for line in data.splitlines():
    record = dict(zip(props, line.split(',')))
    record.pop('_dummy')
    record.pop('accuracy')
    record['location'] = ndb.GeoPt(float(record.pop('lat')),
                                   float(record.pop('lon')))

    for key in ['zip_code', 'enrollment', 'locale_code',
                'school_type', 'school_level']:
      try:
        record[key] = int(record[key])
      except:
        record.pop(key)

    school = PublicSchool(**record)
    school.update_location()
    school.put()


class GeomodelTests(AppTest):
  def test_geo(self):
    _populate_db()

    results = PublicSchool.bounding_box_fetch(
      PublicSchool.query().order(PublicSchool.school_id),
      geotypes.Box(39, -82, 41, -84),
      max_results=10)
    self.assertEqual(len(results), 2)
    self.assertEqual(results[0].school_id, '390000104683')
    self.assertEqual(results[1].school_id, '390000204684')

    results = PublicSchool.bounding_box_fetch(
      PublicSchool.query().order(PublicSchool.school_id),
      geotypes.Box(38, -83, 40, -85),
      max_results=10)
    self.assertEqual(len(results), 1)
    self.assertEqual(results[0].school_id, '390002001515')

    results = PublicSchool.proximity_fetch(
      PublicSchool.query(),
      geotypes.Point(40, -83),
      max_results=10,
      max_distance=50000) # Within 50km.
    self.assertEqual(len(results), 2)
    self.assertEqual(results[0].school_id, '390000104683')
    self.assertEqual(results[1].school_id, '390000204684')

    results = PublicSchool.proximity_fetch(
      PublicSchool.query(),
      geotypes.Point(34, -117),
      max_results=10,
      max_distance=50000) # Within 50km.
    self.assertEqual(len(results), 2)
    self.assertEqual(results[0].school_id, '590019700136')
    self.assertEqual(results[1].school_id, '590010500138')


if __name__ == '__main__':
  unittest.main()
