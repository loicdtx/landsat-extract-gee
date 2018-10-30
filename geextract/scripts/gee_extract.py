#!/usr/bin/env python
from __future__ import print_function

import argparse
from datetime import datetime
from geextract import ts_extract, relabel, date_append, dictlist2sqlite

def main(lon, lat, sensor, begin, end, radius, stats, db, table, site,
         tiers):
    # Parse time string into datetime object
    begin = datetime.strptime(begin, '%Y-%m-%j')
    end = datetime.strptime(end, '%Y-%m-%j')
    # Extract data
    dict_list_0 = ts_extract(lon=lon, lat=lat, sensor=sensor, start=begin, end=end,
                           radius=radius, stats=stats, tiers=tiers)
    print('Extracted %d records from Google Eath Engine' % len(dict_list_0))
    # Prepare list of dictories ()
    dict_list_1 = relabel(dict_list_0, sensor)
    dict_list_2 = date_append(dict_list_1)
    # Write to db
    dictlist2sqlite(dict_list_2, site=site, sensor=sensor, db_src=db, table=table)

if __name__ == '__main__':
    epilog = """
Command line utility to extract Lansat surface reflectance data from the google earth
engine platform and write the output to a local sqlite database. Query can be done for
a single pixel, or for a circular region, in which case data are spatially aggregated
for each time step using the a user defined spatial aggregation function.

sqlite tables get appended if new data are queried (i.e. for the same location but a different sensor).

--------------------------
Example usage
--------------------------
# Extract all the LT5 bands for a location in Yucatan for the entire Landsat period, with a 500m radius
gee_extract.py -s LT5 -b 1980-01-01 -lon -89.8107 -lat 20.4159 -r 500 -db /tmp/gee_db.sqlite -site uxmal -table col_1
gee_extract.py -s LE7 -b 1980-01-01 -lon -89.8107 -lat 20.4159 -r 500 -db /tmp/gee_db.sqlite -site uxmal -table col_1
gee_extract.py -s LC8 -b 1980-01-01 -lon -89.8107 -lat 20.4159 -r 500 -db /tmp/gee_db.sqlite -site uxmal -table col_1

# Extract only tier 1 data for LC8
gee_extract.py -s LC8 -b 1980-01-01 -lon -89.8107 -lat 20.4159 -r 500 -db /tmp/gee_db.sqlite -site uxmal -table col_1 --tiers T1
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

    parser.add_argument('-site', '--site', required=True,
                        help='Label associated with that location (e.g. Site name)')

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

    parser.add_argument('-t', '--tiers', required=False,
                        nargs='*',
                        type=str,
                        default=['T1', 'T2'],
                        help='Tiers to order (T1: highest quality, defaults to T1 and T2)')

    parsed_args = parser.parse_args()

    main(**vars(parsed_args))
