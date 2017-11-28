#!/usr/bin/env python
from __future__ import print_function

import argparse
from datetime import datetime
from geextract import ts_extract, dictlist2sqlite

def main(lon, lat, sensor, begin, end, radius, bands, stats, collection, db,
         table):
    # Parse time string into datetime object
    begin = datetime.strptime(begin, '%Y-%m-%j')
    end = datetime.strptime(end, '%Y-%m-%j')
    # Collection can be a string or an integer, prepare input type for passing to ts_extract
    if collection.isdigit():
        collection = int(collection)
    # Extract data
    dict_list = ts_extract(lon=lon, lat=lat, sensor=sensor, start=begin, end=end,
                           radius=radius, bands=bands, stats=stats,
                           collection=collection)
    print('Extracted %d records from Google Eath Engine' % len(dict_list))
    # Write to db
    dictlist2sqlite(dict_list, db, table)

if __name__ == '__main__':
    epilog = """
Command line utility to extract Lansat surface reflectance data from the google earth
engine platform and write the output to a local sqlite database. Query can be done for
a single pixel, or for a circular region, in which case data are spatially aggregated
for each time step using the a user defined spatial aggregation function.

sqlite tables get appended if new data are queried (i.e. for the same location but a different sensor),
but mind that band names are different for LC8 and the other sensors.

--------------------------
Example usage
--------------------------
# Extract all the LT5 bands for a location in Yucatan for the entire Landsat period, with a 500m radius
gee_extract.py -s LT5 -b 1980-01-01 -lon -89.8107 -lat 20.4159 -r 500 -db /tmp/gee_db.sqlite -table uxmal
# Order pre-collection data
gee_extract.py -s LT5 -b 1980-01-01 -lon -89.8107 -lat 20.4159 -r 500 -db /tmp/gee_db.sqlite -table uxmal_pre -col pre
"""


    parser = argparse.ArgumentParser(epilog=epilog, formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-lat', '--lat',
                        required=True,
                        type=float,
                        help='center latitude in Decimal Degrees')

    parser.add_argument('-lon', '--lon',
                        required=True,
                        type=float,
                        help='center longitude in Decimal Degrees')

    parser.add_argument('-b', '--begin',
                        required = True,
                        help = 'Anterior time-range boundary in yyyy-mm-dd')

    parser.add_argument('-e', '--end',
                        required = False,
                        help = 'Posterior time-range boundary in yyyy-mm-dd')
    parser.set_defaults(end=datetime.today().date().strftime('%Y-%m-%d'))

    parser.add_argument('-db', '--db', required=True,
                        help='Path to sqlite database. Will be created if does not exist')

    parser.add_argument('-table', '--table', required=True,
                        help='Database table name to write data. Existing tables will be appended')

    parser.add_argument('-r', '--radius', type=float, required=False,
                        help='Optional circular radius in meters around center point')
    parser.set_defaults(radius=None)

    parser.add_argument('-s', '--sensor', required=True,
                        help='Landsat sensor to query; one of LT4, LT5, LE7, LC8')

    parser.add_argument('-stats', '--stats', required=False,
                        help='Spatial aggregation function, one of mean (default), median, max or min. Only relevant if a radius value is provided')
    parser.set_defaults(stats='mean')

    parser.add_argument('-col', '--collection', type=str, required=False,
                        help='Landsat collection. \'pre\' for pre-collection, 1 for collection 1 (default)')
    parser.set_defaults(collection='1')

    parser.add_argument('-bands', '--bands', nargs='*', required=False,
                       help='Landsat spectral bands to include in the output. Defaults to all bands (different for LC8 and the other sensors)')
    parser.set_defaults(bands=None)


    parsed_args = parser.parse_args()

    main(**vars(parsed_args))
