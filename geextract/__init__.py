"""geextract"""

__version__ = "0.1"

import ee
import sqlite3
import pandas as pd
import re
from datetime import datetime

ee.Initialize()


def get_date(filename):
    """Retriev date information from typical Landsat filenames

    Args:
        filename (str): Landsat file name

    Returns:
        datetime.date : The corresponding date of the filename.

    Examples:
        >>> import geextract
        >>> geextract.get_date('LC81970292013106')
    """
    pattern = re.compile(r'(?P<sensor>LC8|LE7|LT5|LT4)(?P<pathrow>\d{6})(?P<date>\d{7})')
    m = pattern.search(filename)
    d = datetime.strptime(m.group('date'), '%Y%j').date()
    return d

def ts_extract(lon, lat, sensor, start, end = None, radius = None, bands = None,
               stats = 'mean', cfmask_val = 0):
    """Perform a spatio temporal query to extract Landsat surface reflectance data
        from gee

    Args:
        lon (float): Center longitude in decimal degree
        lat (float): Center latitude in decimal degree
        sensor (str): Landsat sensor to query data from. Must be one of 'LT4',
            'LT5', 'LE7', 'LC8'
        start (datetime.datetime): Start date
        end (datetime.datetime): Optional end date; automatically set as today if unset
        radius (float): Optional radius around center point in meters. If unset,
            time-series of a single pixel are queried. Otherwise a reducer is used
            to spatially aggregate the pixels intersecting the circular feature
            built.
        bands (list): List of Landsat band names. Optional, defaults to
            ['B1', 'B2', 'B3', 'B4', 'B5', 'B7'] in the case of LC8 sensor and to
            ['B1', 'B2', 'B3', 'B4', 'B5', 'B7'] otherwise.
        stats (str): Spatial aggregation function to use. Only relevant
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
    if radius is not None:
        # Define spatial aggregation function
        if stats == 'mean':
            fun = ee.Reducer.mean()
        elif stats == 'median':
            fun = ee.Reducer.median()
        elif stats == 'max':
            fun = ee.Reducer.max()
        elif stats == 'min':
            fun = ee.Reducer.min()
        else:
            raise ValueError('Unknown spatial aggregation function. Must be one of mean, median, max, or min')

        geometry = ee.Geometry.Point(lon, lat).buffer(radius)
        # Define function to map over imageCollection to perform spatial aggregation 
        def _reduce_region(image):
            """Spatial aggregation function for a single image and a polygon feature"""
            stat_dict = image.reduceRegion(fun, geometry, 30);
            # FEature needs to be rebuilt because the backend doesn't accept to map
            # functions that return dictionaries
            return ee.Feature(None, stat_dict)
        fc = landsat.filterBounds(geometry).map(_reduce_region).getInfo()
        out = simplify(fc)
    else:
        # Extraction with a point, no spatial aggregation, etc
        geometry = ee.Geometry.Point(lon, lat)
        l = landsat.filterBounds(geometry).getRegion(geometry, 30).getInfo()
        out = dictify(l)
    return out

def simplify(fc):
    """Take a feature collection, as returned by mapping a reducer to a ImageCollection,
        and reshape it into a simpler list of dictionaries

    Args:
        fc (dict): Dictionary representation of a feature collection, as returned
            by mapping a reducer to an ImageCollection

    Returns:
        list: A list of dictionaries.

    Examples:
        >>> fc = {u'columns': {},
        ...       u'features': [{u'geometry': None,
        ...                      u'id': u'LC81970292013106',
        ...                      u'properties': {u'B1': 651.8054424353023,
        ...                                      u'B2': 676.6018246419446},
        ...                      u'type': u'Feature'},
        ...                     {u'geometry': None,
        ...                      u'id': u'LC81970292013122',
        ...                      u'properties': {u'B1': 176.99323997958842,
        ...                                      u'B2': 235.83196553144882},
        ...                      u'type': u'Feature'}]}
        >>> simplify(fc)
    """
    def feature2dict(f):
        id = f['id']
        out = f['properties']
        out.update(id=id)
        return out
    out = [feature2dict(x) for x in fc['features']]
    return out

def dictify(x):
    """Build a list of dictionaries from a list of lists as returned by running
        getRegion on an Image collection

    Args:
        x (list): A list of list. First list element contain the keys while following
            list elements contain values.

    Returns:
        list: A list of dictionaries

    Examples:
        >>> l = [[u'id', u'B1', u'B2', u'B3', u'B7'],
        ...      [u'LC81970292013106', 649, 683, 910, 1365],
        ...      [u'LC81970292013122', 140, 191, 521, 965]]
        >>> dictify(l)
    """
    out = [dict(zip(x[0], values)) for values in x[1:]]
    return out

def date_append(dl):
    pass

def dictlist2sqlite(dl, db_src, table):
    """Write a list of dictionaries to a sqlite database

    Args:
        dl (list): List of dictionaries
        db_src (str): Path an sqlite database (created in case it does not exist)
        table (str): Name of database table to write data

    Returns:
        This function is used for its side effect of writing data to a database;
            it does not return anything
    """
    df = pd.Dataframe(dl)
    con = sqlite3.connect(db_src)
    df.to_sql(name=table, con=con, if_exists='append')

