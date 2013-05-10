import unittest
from models import *
from app import *
from helpers import *
from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed
import webtest
class TestNDB(unittest.TestCase):
    
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
        test_meter = ParkingMeter(location=ndb.GeoPt(float(40.1164), float(88.2433)),
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
        self.test_meter = ParkingMeter(location=ndb.GeoPt(float(41.8500), float(87.6500)),
                                         time_limit=60,
                                         time_per_quarter=15,
                                         enforcement_start=8,
                                         enforcement_end=6,
                                         congestion=1)
        self.test_meter.update_location()
        self.test_meter.put()

    def tearDown(self):
        self.testbed.deactivate()
        
    def test_getwebb(self):
        #tests that everything responds
        result = self.testapp.get("/")
        self.assertEqual(result.status, "200 OK")
        result = self.testapp.get("/request")
        self.assertEqual(result.status, "200 OK")
        result = self.testapp.get("/request?new_request=Scott+Park%2C+Champaign%2C+IL")
        self.assertEqual(result.status, "200 OK")
        result = self.testapp.get("/request?new_request=Scott+Park%2C+Champaign%2C+IL")
        self.assertEqual(result.status, "200 OK")
        result = self.testapp.get("/route?destination=Scott+Park%2C+Champaign%2C+IL")
        self.assertEqual(result.status, "200 OK")      
        result = self.testapp.get("/setup?command=populate")
        self.assertEqual(result.status, "200 OK")
        
    def test_postwebb(self):
        postData = {'key' : self.test_meter.key.id(), 'time_limit' : 60, 
                                'time_per_quarter' : 15, 
                                'enforcement_start' : 8,
                                'enforcement_end' : 6,
                                'congestion' : 1
                                }
        result = self.testapp.post("/update", postData)
        self.assertEqual(result.status, "200 OK")
        postData['congestion'] = -1
        result=self.testapp.post("/update",postData)
        self.assertEqual(result.status, "200 OK")
        postData['congestion'] = 11
        result=self.testapp.post("/update",postData)
        self.assertEqual(result.status, "200 OK")
        postData['congestion'] = 1
        postData['time_limit'] = 1000
        result=self.testapp.post("/update",postData)
        self.assertEqual(result.status, "200 OK")
        postData['time_limit'] = -1
        result=self.testapp.post("/update",postData)
        self.assertEqual(result.status, "200 OK")

class TestHelpers(unittest.TestCase):
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
        
    def test_makeMeterDict(self):
        meter = ParkingMeter(location=ndb.GeoPt(float(41.8500), float(87.6500)),
                                         time_limit=60,
                                         time_per_quarter=15,
                                         enforcement_start=8,
                                         enforcement_end=6,
                                         congestion=1)
        meter.update_location()
        meter.put()

        key = meter.key.id()
        lat = meter._get_latitude()
        lon = meter._get_longitude()
        time_limit = meter.time_limit
        time_per_quarter = meter.time_per_quarter
        enforcement_start = meter.enforcement_start
        enforcement_end = meter.enforcement_end
        congestion = meter.congestion

        meter_dict = makeMeterDict(meter)
        
        self.assertEqual(meter_dict['key'], key)
        self.assertEqual(meter_dict['lat'], lat)
        self.assertEqual(meter_dict['lon'], lon)
        self.assertEqual(meter_dict['time_limit'], time_limit)
        self.assertEqual(meter_dict['time_per_quarter'], time_per_quarter)
        self.assertEqual(meter_dict['enforcement_start'], enforcement_start)
        self.assertEqual(meter_dict['enforcement_end'], enforcement_end)
        self.assertEqual(meter_dict['congestion'], congestion)

    def test_populate(self):
        populate()
        qry = ParkingMeter.query()
        meter = qry.fetch(limit=1)
        self.assertNotEqual(meter, None)

    def test_geocode(self):
        coded_string = geocode("Scott Park, Champaign")
        self.assertEqual(coded_string[0], "Scott Park, Champaign, IL 61820, USA")
    


        



if __name__ == '__main__':
    unittest.main()
