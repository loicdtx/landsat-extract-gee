#!/usr/bin/env python
from __future__ import print_function

import argparse
from datetime import datetime
import csv
from geextract import ts_extract, dictlist2sqlite, relabel, date_append

def main(file, sensor, begin, end, radius, stats, db, table, tiers):
    # Parse time string into datetime object
    begin = datetime.strptime(begin, '%Y-%m-%j')
    end = datetime.strptime(end, '%Y-%m-%j')
    # Read coordinates and table names from text file
    with open(file) as src:
        reader = csv.reader(src)
        for line in reader:
            try:
                lon = float(line[0])
                lat = float(line[1])
                site = line[2]
                # Extract data
                dict_list_0 = ts_extract(lon=lon, lat=lat, sensor=sensor,
                                         start=begin, end=end, radius=radius,
                                         stats=stats, tiers=tiers)
                print('Extracted %d records from Google Eath Engine' % len(dict_list_0))
                # Prepare list of dictories ()
                dict_list_1 = relabel(dict_list_0, sensor)
                dict_list_2 = date_append(dict_list_1)
                # Write to db
                dictlist2sqlite(dict_list_2, site=site, sensor=sensor, db_src=db, table=table)
            except Exception as e:
                print('An error occured while extracting a site. %s' % e)

if __name__ == '__main__':
    epilog = """
Command line utility to batch extract Lansat surface reflectance data from the google earth
engine platform and write the output to a local sqlite database. Query can be done for
a single pixel, or for a circular region, in which case data are spatially aggregated
for each time step using the a user defined spatial aggregation function.

Input locations must be provided in a text file, with on each line lon,lat,site_name
site_name provided for each site in the text file is used (together with sensor) as grouping variable
in the sqlite table.

--------------------------
Example usage
--------------------------
# Extract all the LC8 bands in a 500 meters for two locations between 2012 and now
echo "4.7174,44.7814,rompon\\n-149.4260,-17.6509,tahiti" > site_list.txt
gee_extract_batch.py site_list.txt -b 1984-01-01 -s LT5 -r 500 -db /tmp/gee_db.sqlite -table landsat_ts
gee_extract_batch.py site_list.txt -b 1984-01-01 -s LE7 -r 500 -db /tmp/gee_db.sqlite -table landsat_ts
gee_extract_batch.py site_list.txt -b 1984-01-01 -s LC8 -r 500 -db /tmp/gee_db.sqlite -table landsat_ts

# Only Tier 1 for LC8
gee_extract_batch.py site_list.txt -b 1984-01-01 -s LC8 -r 500 -db /tmp/gee_db.sqlite -table landsat_ts --tiers T1
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

    parser.add_argument('-table', '--table', required=True,
                        help='Database table name to write data. Existing tables will be appended')

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

