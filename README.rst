geextract
=========

*Google Earth Engine data extraction tool. Quickly obtain Landsat multispectral time-series for exploratory analysis and algorithm testing*

Online documentation available at https://loicdtx.github.io/landsat-extract-gee

.. image:: https://coveralls.io/repos/github/loicdtx/landsat-extract-gee/badge.svg?branch=master
    :target: https://coveralls.io/github/loicdtx/landsat-extract-gee?branch=master

.. image:: https://travis-ci.org/loicdtx/landsat-extract-gee.svg?branch=master
    :target: https://travis-ci.org/loicdtx/landsat-extract-gee

.. image:: https://badge.fury.io/py/geextract.svg
    :target: https://badge.fury.io/py/geextract



Introduction
------------


A python library (API + command lines) to extract Landsat time-series from the Google Earth Engine platform. Can query single pixels or spatially aggregated values over polygons. When used via the command line, extracted time-series are written to a sqlite database.

The idea is to provide quick access to Landsat time-series for exploratory analysis or algorithm testing. Instead of downloading the whole stack of Landsat scenes, preparing the data locally and extracting the time-series of interest, which may take several days, ``geextract`` allows to get time-series in a few seconds.

Compatible with python 2.7 and 3.

Usage
-----

API
^^^

The principal function of the API is ``ts_extract``

.. code-block:: python

    from geextract import ts_extract
    from datetime import datetime

    # Extract a Landsat 7 time-series for a 500m radius circular buffer around
    # a location in Yucatan
    lon = -89.8107197
    lat = 20.4159611
    LE7_dict_list = ts_extract(lon=lon, lat=lat, sensor='LE7',
                               start=datetime(1999, 1, 1), radius=500)


Command line
^^^^^^^^^^^^

``geextract`` comes with two command lines, for extracting Landsat time-series directly from the command line.

- ``gee_extract.py``: Extract a Landsat multispectral time-series for a single site. Extracted data are automatically added to a sqlite database.
- ``gee_extract_batch.py``: Batch order Landsat multispectral time-series for multiple locations.
  
.. code-block:: bash
    
    gee_extract.py --help

    # Extract all the LT5 bands for a location in Yucatan for the entire Landsat period, with a 500m radius
    gee_extract.py -s LT5 -b 1980-01-01 -lon -89.8107 -lat 20.4159 -r 500 -db /tmp/gee_db.sqlite -site uxmal -table col_1
    gee_extract.py -s LE7 -b 1980-01-01 -lon -89.8107 -lat 20.4159 -r 500 -db /tmp/gee_db.sqlite -site uxmal -table col_1
    gee_extract.py -s LC8 -b 1980-01-01 -lon -89.8107 -lat 20.4159 -r 500 -db /tmp/gee_db.sqlite -site uxmal -table col_1

.. code-block:: bash

    gee_extract_batch.py --help

    # Extract all the LC8 bands in a 500 meters for two locations between 2012 and now
    echo "4.7174,44.7814,rompon\n-149.4260,-17.6509,tahiti" > site_list.txt
    gee_extract_batch.py site_list.txt -b 1984-01-01 -s LT5 -r 500 -db /tmp/gee_db.sqlite -table landsat_ts
    gee_extract_batch.py site_list.txt -b 1984-01-01 -s LE7 -r 500 -db /tmp/gee_db.sqlite -table landsat_ts
    gee_extract_batch.py site_list.txt -b 1984-01-01 -s LC8 -r 500 -db /tmp/gee_db.sqlite -table landsat_ts


.. image:: https://github.com/loicdtx/landsat-extract-gee/raw/master/docs/figs/multispectral_uxmal.png




Installation
------------

You must have a `Google Earth Engine <http://signup.earthengine.google.com/#!/>`__ account to use the package.

Then, in a vitual environment run:

.. code-block:: bash

    pip install geextract
    earthengine authenticate


This will open a google authentication page in your browser, and will give you an authentication token to paste back in the terminal.

You can check that the authentication process was successful by running.

.. code-block:: bash

    python -c "import ee; ee.Initialize()"


If nothing happens... it's working.


Benchmark
---------

A quick benchmark of the extraction speed, using a 500 m buffer.

.. code-block:: python

    import time
    from datetime import datetime
    from pprint import pprint
    import geextract

    lon = -89.8107197
    lat = 20.4159611

    for sensor in ['LT5', 'LE7', 'LT4', 'LC8']:
        start = time.time()
        out = geextract.ts_extract(lon=lon, lat=lat, sensor=sensor, start=datetime(1980, 1, 1, 0, 0),
                                   end=datetime.today(), radius=500)
        end = time.time()

        pprint('%s. Extracted %d records in %.1f seconds' % (sensor, len(out), end - start))

.. code-block:: pycon

    # 'LT5. Extracted 142 records in 1.9 seconds'
    # 'LE7. Extracted 249 records in 5.8 seconds'
    # 'LT4. Extracted 7 records in 1.0 seconds'
    # 'LC8. Extracted 72 records in 2.4 seconds'
