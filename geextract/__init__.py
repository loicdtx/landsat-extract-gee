"""geextract"""

__version__ = "0.1"

import ee
import sqlite3
import pandas as pd
import csv

ee.Initialize()

# Plan:
    # 1-ts_extract
    # 2-json2db
    # 3-

def ts_extract(lon, lat, sensor, start, end = None, radius = None, bands = None,
               stats = ['mean', 'median'], cfmask_val = 0):
    """Perform a spatio temporal query to extract Landsat surface reflectance data
        from gee

    Args:
        lon (float): Center longitude in decimal degree
        lat (float): Center latitude in decimal degree
        sensor (str): Landsat sensor to query data from. Must be one of 'LT4',
            'LT5', 'LE7', 'LC8'
        start (datetime.date): Start date
        end (datetime.date): Optional end date; automatically set as today if unset
        radius (float): Optional radius around center point in meters. If unset,
            time-series of a single pixel are queried. Otherwise a reducer is used
            to spatially aggregate the pixels intersecting the circular feature
            built.
        bands (list): List of Landsat band names. Optional, defaults to
            ['B1', 'B2', 'B3', 'B4', 'B5', 'B7'] in the case of LC8 sensor and to
            ['B1', 'B2', 'B3', 'B4', 'B5', 'B7'] otherwise.
        stats (list): List of spatial aggregating functions to use. Only relevant
            if a radius value is set.
        cfmask_val (int): Value of the cfmask band corresponding to valid pixels.
            Defaults to 0.

    Returns:
        dict: A dictionary representation of the json data returned by the gee platform.
    """
    # Define some internal functions to be mapped over imageCollections
    def _mask_clouds(image):
        """Cloud masking function"""
        invalid = image.select('cfmask').neq(cfmask_val)
        return image.mask(invalid.Not())

    # Check inputs
    if sensor not in ['LT4', 'LT5', 'LC8', 'LE7']:
        raise ValueError('Unknown sensor (Must be one of LT4, LT5, LE7, LC8)')
    if bands is None:
        if sensor in ['LT4', 'LT5', 'LE7']:
            bands = ['B1', 'B2', 'B3', 'B4', 'B5', 'B7']
        else:
            bands = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7']
    sensor = 'LANDSAT/%s_SR' % sensor
    # Prepare image collection
    landsat = ee.ImageCollection(sensor).\
            filterDate(start=start, opt_end=end)\
            .map(_mask_clouds)\
            .select(bands)
    geometry = ee.Geometry.Point(lon, lat)
    if radius is not None:
        geometry = geometry.buffer(radius)

    # col = ee.ImageCollection(product).\
    # select(bands).\
    # filterDate(start_date, end_date)
# 
    # data = col.getRegion(geometry, int(res)).getInfo()
# 
# 
# def dict2db(in_dict, con, name):
# df = pd.DataFrame.from_records(data[1:])
# df.columns = data[0]
# con = sqlite3.connect(db_src)
# df.to_sql(name=table_name, con=con, if_exists='append')

