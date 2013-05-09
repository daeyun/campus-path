import unittest
from models import *
from app import *
from helpers import *
from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed

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
        meter_key = str(test_meter.put())

        returned_meter = ParkingMeter.get(meter_key)
        
        lat = test_meter._get_latitude()
        lon = test_meter._get_longitude()
        self.assertEqual(41.8500, lat)
        self.assertEqual(87.6500,lat)


        
if __name__ == '__main__':
    unittest.main()
