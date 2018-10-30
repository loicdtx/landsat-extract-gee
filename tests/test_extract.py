from geextract import ts_extract
import unittest
from datetime import datetime

class TestTsExtraction(unittest.TestCase):
    def test_point(self):
        a = ts_extract(lon=4.722111, lat=44.770928, sensor='LC8', start=datetime(2015,1,1),
                       end=datetime(2016, 6, 1), radius = None, feature = None, bands = None,
                       stats = 'mean')
        self.assertTrue(len(a) > 2)
        self.assertTrue(isinstance(a[0], dict))
        self.assertEqual(set(a[0].keys()),
                         set(['id', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7']))

    def test_point_radius(self):
        a = ts_extract(lon=-3, lat=44.7, sensor='LC8', start=datetime(2015,1,1),
                       end=datetime(2016, 6, 1), radius = 300, feature = None, bands = None,
                       stats = 'mean')
        self.assertTrue(len(a) > 2)
        self.assertTrue(isinstance(a[0], dict))
        self.assertEqual(set(a[0].keys()),
                         set(['id', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7']))

    def test_point_radius_tm(self):
        a = ts_extract(lon=-3, lat=44.7, sensor='LT5', start=datetime(1999,1,1),
                       end=datetime(2005, 6, 1), radius = 300, feature = None, bands = None,
                       stats = 'median')
        self.assertTrue(len(a) > 2)
        self.assertTrue(isinstance(a[0], dict))
        self.assertEqual(set(a[0].keys()),
                         set(['id', 'B1', 'B2', 'B3', 'B4', 'B5', 'B7']))

    def test_point_radius_tiers(self):
        a = ts_extract(lon=-3, lat=44.7, sensor='LC8', start=datetime(2015,1,1),
                       end=datetime(2016, 6, 1), radius = 300, feature = None, bands = None,
                       stats = 'mean', tiers=['T1'])
        self.assertTrue(len(a) > 2)
        self.assertTrue(isinstance(a[0], dict))
        self.assertEqual(set(a[0].keys()),
                         set(['id', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7']))

    def test_point_radius_tm_tiers(self):
        a = ts_extract(lon=-3, lat=44.7, sensor='LT5', start=datetime(1999,1,1),
                       end=datetime(2010, 6, 1), radius = 300, feature = None, bands = None,
                       stats = 'median', tiers=['T1'])
        self.assertTrue(len(a) > 2)
        self.assertTrue(isinstance(a[0], dict))
        self.assertEqual(set(a[0].keys()),
                         set(['id', 'B1', 'B2', 'B3', 'B4', 'B5', 'B7']))

    def test_exceptions(self):
        # sensor does not exist
        kwargs_1 = {'lon': -3,
                  'lat': 44.7,
                  'sensor': 'LT8',
                  'start': datetime(1999, 1, 1),
                  'end': datetime(2000, 6, 1),
                  'radius': 300,
                  'stats': 'max'}
        self.assertRaises(ValueError, ts_extract, **kwargs_1)
        # aggregation method does not exist
        kwargs_2 = {'lon': -3,
                  'lat': 44.7,
                  'sensor': 'LT5',
                  'start': datetime(1999, 1, 1),
                  'end': datetime(2000, 6, 1),
                  'radius': 300,
                  'stats': 'mode'}
        self.assertRaises(ValueError, ts_extract, **kwargs_2)
