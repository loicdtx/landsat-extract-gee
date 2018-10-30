from geextract import ts_extract, relabel, date_append, dictlist2sqlite
import fiona
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import sqlite3
from datetime import datetime
import os

try:
    os.remove('/tmp/landsat_cdmx.sqlite')
except:
    pass

# Open feature collection generator
with fiona.open('data/cdmx_parks.gpkg', layer='parks') as src:
    # Iterate over feature collection
    for feature in src:
        # Extract time-series
        ts_0 = ts_extract(sensor='LC8', start=datetime(2012, 1, 1),
                          feature=feature)
        ts_1 = relabel(ts_0, 'LC8')
        ts_2 = date_append(ts_1)
        # Write dictionnary list to sqlite database table
        dictlist2sqlite(ts_2, site=feature['properties']['name'],
                        sensor='LC8', db_src='/tmp/landsat_cdmx.sqlite',
                        table='cdmx')

# REad the data back into a pandas dataframe
conn = sqlite3.connect("/tmp/landsat_cdmx.sqlite")
df = pd.read_sql_query('select * from cdmx', conn)
df['date'] = pd.to_datetime(df['time'], format='%Y-%m-%d')
df['ndvi'] = (df.nir - df.red) / (df.nir + df.red)
# Make facetgrid plot
g = sns.FacetGrid(df, row='site', aspect=4, size=2)
def dateplot(x, y, **kwargs):
    ax = plt.gca()
    data = kwargs.pop("data")
    data.plot(x=x, y=y, ax=ax, grid=False, **kwargs)
g = g.map_dataframe(dateplot, "date", "ndvi")
plt.show()