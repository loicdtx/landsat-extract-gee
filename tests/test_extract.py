from geextract import ts_extract
import unittest
from datetime import datetime

class TestTsExtraction(unittest.TestCase):
    def test_point(self):
        a = ts_extract(lon=4.722111, lat=44.770928, sensor='LC8', start=datetime(2015,1,1),
                       end=datetime(2016, 6, 1), radius = None, feature = None, bands = None,
                       stats = 'mean', collection = 1)
        self.assertTrue(len(a) > 2)
        self.assertTrue(isinstance(a[0], dict))
        self.assertEqual(set(a[0].keys()),
                         set(['id', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'latitude',
                              'longitude', 'time']))

    def test_point_radius(self):
        a = ts_extract(lon=-3, lat=44.7, sensor='LC8', start=datetime(2015,1,1),
                       end=datetime(2016, 6, 1), radius = 300, feature = None, bands = None,
                       stats = 'mean', collection = 1)
        self.assertTrue(len(a) > 2)
        self.assertTrue(isinstance(a[0], dict))
        self.assertEqual(set(a[0].keys()),
                         set(['id', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7']))

