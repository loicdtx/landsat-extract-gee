#!/usr/bin/env python
from __future__ import print_function

import argparse
from datetime import datetime
import csv
from geextract import ts_extract, dictlist2sqlite

def main(file, sensor, begin, end, radius, bands, stats, collection, db):
    # Parse time string into datetime object
    begin = datetime.strptime(begin, '%Y-%m-%j')
    end = datetime.strptime(end, '%Y-%m-%j')
    # Collection can be a string or an integer, prepare input type for passing to ts_extract
    if collection.isdigit():
        collection = int(collection)
    # Read coordinates and table names from text file
    with open(file) as src:
        reader = csv.reader(src)
        for line in reader:
            try:
                lon = float(line[0])
                lat = float(line[1])
                table = '%s_%s' % (line[2], sensor)
                # Extract data
                dict_list = ts_extract(lon=lon, lat=lat, sensor=sensor, start=begin, end=end,
                                       radius=radius, bands=bands, stats=stats,
                                       collection=collection)
                print('Extracted %d records from Google Eath Engine' % len(dict_list))
                # Write to db
                dictlist2sqlite(dict_list, db, table)
            except Exception as e:
                print('An error occured while extracting a site. %s' % e)

if __name__ == '__main__':
    epilog = """
Command line utility to batch extract Lansat surface reflectance data from the google earth
engine platform and write the output to a local sqlite database. Query can be done for
a single pixel, or for a circular region, in which case data are spatially aggregated
for each time step using the a user defined spatial aggregation function.

Input locations must be provided in a text file, with on each line lon,lat,site_name
site_name provided for each site in the text file is used as table names, with sensor name
appended.

--------------------------
Example usage
--------------------------
# Extract all the LC8 bands in a 500 meters for two locations between 2012 and now
echo "4.7174,44.7814,rompon\\n-149.4260,-17.6509,tahiti" > site_list.txt
gee_extract_batch.py site_list.txt -b 2012-01-01 -s LC8 -r 500 -db /tmp/gee_db.sqlite
"""


    parser = argparse.ArgumentParser(epilog=epilog, formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('file', type=str,
                        help='Input text file with coma separated site coordinates in DD and site name on each line.')

    parser.add_argument('-b', '--begin',
                        required = True,
                        help = 'Anterior time-range boundary in yyyy-mm-dd')

    parser.add_argument('-e', '--end',
                        required = False,
                        help = 'Posterior time-range boundary in yyyy-mm-dd')
    parser.set_defaults(end=datetime.today().date().strftime('%Y-%m-%d'))

    parser.add_argument('-db', '--db', required=True,
                        help='Path to sqlite database. Will be created if does not exist')

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

