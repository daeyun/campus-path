import unittest
from models import *
from app import *
from helpers import *
from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed
import webtest
class TestApp(unittest.TestCase):
    
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()
                
    def test_get(self):
        test_meter = ParkingMeter(location=ndb.GeoPt(float(41.8500), float(87.6500)),
                                         time_limit=60,
                                         time_per_quarter=15,
                                         enforcement_start=8,
                                         enforcement_end=6,
                                         congestion=1)
        test_meter.update_location()
        meter_key = test_meter.put()

        returned_meter = meter_key.get()        
        lat = returned_meter._get_latitude()
        lon = returned_meter._get_longitude()
        atts = returned_meter.public_attributes()
        self.assertEqual(41.8500, lat)
        self.assertEqual(87.6500,lon)
        self.assertEqual(atts[0], 'time_limit')
        self.assertEqual(atts[1], 'time_per_quarter')
        self.assertEqual(atts[2], 'enforcement_start')
        self.assertEqual(atts[3], 'enforcement_end')
        self.assertEqual(atts[4], 'congestion')
        
    def test_set(self):
        test_meter = ParkingMeter(location=ndb.GeoPt(float(41.8500), float(87.6500)),
                                         time_limit=60,
                                         time_per_quarter=15,
                                         enforcement_start=8,
                                         enforcement_end=6,
                                         congestion=1)
        test_meter.update_location()
        meter_key = test_meter.put()
        returned_meter = meter_key.get()
        returned_meter._set_latitude(40.1164)
        returned_meter._set_longitude(88.2433)
        
        lat_orig = test_meter._get_latitude()
        lon_orig = test_meter._get_longitude()
        lat = returned_meter._get_latitude()
        lon = returned_meter._get_longitude()
        
        #Test that the object is changed no matter the reference
        self.assertEqual(40.1164,lat)
        self.assertEqual(88.2433,lon)
        self.assertEqual(40.1164,lat_orig)
        self.assertEqual(88.2433,lon_orig)


class TestHandlers(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.setup_env(app_id='illiniparking')
        self.testbed.activate()
        self.testapp = webtest.TestApp(app)
        self.testbed.init_urlfetch_stub()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()
        
    def test_getwebb(self):
        #tests that everything responds
        result = self.testapp.get("/")
        self.assertEqual(result.status, "200 OK")
        result = self.testapp.get("/request")
        self.assertEqual(result.status, "200 OK")
        result = self.testapp.get("/route?destination=Scott+Park%2C+Champaign%2C+IL")
        self.assertEqual(result.status, "200 OK")
        postData = {'key' : 1, 'time_limit' : 60, 
                                'time_per_quarter' : 15, 
                                'enforcement_start' : 8,
                                'enforcement_end' : 6,
                                'congestion' : 1
                                }
        #result = self.testapp.post("/update", postData)
        #self.assertEqual(result.status, "200 OK")
        #postData.key='new'       
        result = self.testapp.get("/setup?command=populate")
        self.assertEqual(result.status, "200 OK")
if __name__ == '__main__':
    unittest.main()