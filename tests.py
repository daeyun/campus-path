import unittest
from models import *
from app import *
from helpers import *

class TestModel(unittest.TestCase):

    def setUp(self):
        self.test_meter = ParkingMeter(location=ndb.GeoPt(float(41.8500), float(87.6500)),
                                         time_limit=60,
                                         time_per_quarter=15,
                                         enforcement_start=8,
                                         enforcement_end=6,
                                         congestion=1)
    def test_get(self):
        lat = self.test_meter._get_latitude()
        lon = self.test_meter._get_longitude()
        self.assertEqual(41.8500, lat)
        self.assertEqual(87.6500,lat)
                
class TestApp(unittest.TestCase):
    
    def setUp(self):
        
class TestHelpers(unittest.TestCase):

    def setUp(self):
