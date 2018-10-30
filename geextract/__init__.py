"""geextract"""

__version__ = "0.5.0"

import ee
import sqlite3
import pandas as pd
import re
from datetime import datetime
import warnings

# Silence pandas warning
warnings.simplefilter(action='ignore')

ee.Initialize()


BANDS_TO_COLORS = {'LT4': {'B1': 'blue',
                           'B2': 'green',
                           'B3': 'red',
                           'B4': 'nir',
                           'B5': 'swir1',
                           'B7': 'swir2',
                           'id': 'id'},
                   'LC8': {'B2': 'blue',
                           'B3': 'green',
                           'B4': 'red',
                           'B5': 'nir',
                           'B6': 'swir1',
                           'B7': 'swir2',
                           'id': 'id'}}

BANDS_TO_COLORS['LT5'] = BANDS_TO_COLORS['LT4']
BANDS_TO_COLORS['LE7'] = BANDS_TO_COLORS['LT4']


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
    p0 = re.compile(r'(?P<sensor>LC8|LE7|LT5|LT4)(?P<pathrow>\d{6})(?P<date>\d{7})')
    p1 = re.compile(r'(?P<sensor>LC08|LE07|LT04|LT05)_(?P<pathrow>\d{6})_(?P<date>\d{8})')
    if p0.search(filename):
        m = p0.search(filename)
        d = datetime.strptime(m.group('date'), '%Y%j').date()
    elif p1.search(filename):
        m = p1.search(filename)
        d = datetime.strptime(m.group('date'), '%Y%m%d').date()
    else:
        raise ValueError('Unknown pattern')
    return d


def ts_extract(sensor, start, tiers = ['T1', 'T2'], lon = None, lat = None,
               end = datetime.today(), radius = None, feature = None,
               bands = None, stats = 'mean'):
    """Perform a spatio temporal query to extract Landsat surface reflectance data
        from gee

    Args:
        lon (float): Center longitude in decimal degree
        lat (float): Center latitude in decimal degree
        sensor (str): Landsat sensor to query data from. Must be one of 'LT4',
            'LT5', 'LE7', 'LC8'
        tiers (list): List of tiers to order. ``'T1'`` corresponds to tiers 1.
            Default is ``['T1', 'T2']``
        start (datetime.datetime): Start date
        end (datetime.datetime): Optional end date; automatically set as today if unset
        radius (float): Optional radius around center point in meters. If unset,
            time-series of a single pixel are queried. Otherwise a reducer is used
            to spatially aggregate the pixels intersecting the circular feature
            built.
        feature (dict): Optional dictionary representation of a polygon feature
            in longlat CRS. If unset, time-series of a single pixel are queried.
            Otherwise a reducer is used to spatially aggregate the pixels intersecting
            the given feature.
        bands (list): List of Landsat band names. Optional, defaults to
            ['B1', 'B2', 'B3', 'B4', 'B5', 'B7'] in the case of LC8 sensor and to
            ['B1', 'B2', 'B3', 'B4', 'B5', 'B7'] otherwise.
        stats (str): Spatial aggregation function to use. Only relevant
            if a radius value is set.

    Returns:
        dict: A dictionary representation of the json data returned by the gee platform.

    Example:
        >>> import geextract
        >>> from pprint import pprint
        >>> from datetime import datetime

        >>> lon = -89.8107197
        >>> lat = 20.4159611

        >>> out = geextract.ts_extract(lon=lon, lat=lat, sensor='LE7', start=datetime(1980, 1, 1, 0, 0),
        >>>                            radius=500)
        >>> pprint(out)

    """
    # Define some internal functions to be mapped over imageCollections
    def _mask_clouds(image):
        """Cloud masking function"""
        # collection 1 cloud masking example
        # https://code.earthengine.google.com/52e39cc00de3471c905509e374c52284

        # Pre collecction masking example
        # https://code.earthengine.google.com/37ffd688d1b2d2c977fa5c536a023356
        # collection must be a variable of the parent environment
        clear = image.select('pixel_qa').bitwiseAnd(0x2).neq(0)
        valid_range_mask = image.gte(0).And(image.lte(10000))
        return image.updateMask(clear).updateMask(valid_range_mask)

    # Check inputs
    if sensor not in ['LT4', 'LT5', 'LC8', 'LE7']:
        raise ValueError('Unknown sensor (Must be one of LT4, LT5, LE7, LC8)')
    if bands is None:
        if sensor in ['LT4', 'LT5', 'LE7']:
            bands = ['B1', 'B2', 'B3', 'B4', 'B5', 'B7']
        else:
            bands = ['B2', 'B3', 'B4', 'B5', 'B6', 'B7']
    sensor = re.sub(r'(LC|LT|LE)(\d{1})', r'\g<1>0\g<2>', sensor)
    collection_name_template = 'LANDSAT/%s/C01/%%s_SR' % sensor
    # Iterate over tiers to load and merge all corresponding image collections
    landsat_ic = ee.ImageCollection(collection_name_template % tiers[0])
    for tier in tiers[1:]:
        tier_ic = ee.ImageCollection(collection_name_template % tier)
        landsat_ic = ee.ImageCollection(landsat_ic.merge(tier_ic))
    # Prepare image collection
    landsat = landsat_ic.\
            filterDate(start=start, opt_end=end)\
            .map(_mask_clouds)\
            .select(bands)
    if radius is not None or feature is not None:
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

        if feature is not None:
            geometry = ee.Geometry.Polygon(feature['geometry']['coordinates'])
        else: # Geometry defined by point and radius
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
        # pop longitude and lattitude keys from dict collection so that band aliases can
        # be replaced by their color names
        [d.pop('longitude', None) for d in out]
        [d.pop('latitude', None) for d in out]
        [d.pop('time', None) for d in out]
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


def relabel(dl, sensor):
    """Rename the keys of each element of a list of dictionaries

    Args:
        dl (list): List of dictionaries
        sensor (str): Landsat sensor to which belong the data. Must be one of
            'LT4', 'LT5', 'LE7' or 'LC8'

    Returns:
        list: A list of dictionaries
    """
    def change_keys(d, dr):
        return dict((dr[key], value) for (key, value) in d.items())
    dl_out = [change_keys(d, BANDS_TO_COLORS[sensor]) for d in dl]
    return dl_out


def date_append(dl):
    """Add time key to each element of a list of dictionaries

    Args:
        dl (list): List of dictionaries, each dictionary should at least contain
            the key 'id' in which a classic Landsat scene ID parsable by get_date
            is stored.

    Returns:
        list: A list of dictionaries
    """
    # Add time key to each dict of dl
    for item in dl:
        item.update(time = get_date(item['id']))
    return dl


def dictlist2sqlite(dl, site, sensor, db_src, table):
    """Write a list of dictionaries to a sqlite database

    Args:
        dl (list): List of dictionaries
        db_src (str): Path an sqlite database (created in case it does not exist)
        table (str): Name of database table to write data

    Returns:
        This function is used for its side effect of writing data to a database;
            it does not return anything
    """
    df = pd.DataFrame(dl)
    # Drop any row that contain no-data
    # TODO: Filter only row for which all bands are Nan
    df2 = df.dropna(how='any')
    df2['sensor'] = sensor
    df2['site'] = site
    con = sqlite3.connect(db_src)
    df2.to_sql(name=table, con=con, if_exists='append')

