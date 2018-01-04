from geextract import ts_extract, get_date
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
plt.figure(figsize=(10,5))

# Extract a Landsat 7 time-series for a 500m radius circular buffer around
# a location in Yucatan
lon = -89.8107197
lat = 20.4159611
raw_dict = ts_extract(lon=lon, lat=lat, sensor='LE7',
                      start=datetime(1999, 1, 1), radius=500)

# Function to compute ndvi from a dictionary of the list of dictionaries returned
# by ts_extract
def ndvi(x):
    try:
        return (x['B4'] - x['B3']) / (x['B4'] + x['B3'])
    except:
        pass

# Build x and y arrays and remove missing values
x = np.array([get_date(d['id']) for d in raw_dict])
y = np.array([ndvi(d) for d in raw_dict], dtype=np.float)
x = x[~np.isnan(y)]
y = y[~np.isnan(y)]

# Make plot
plt.plot_date(x, y, "--")
plt.plot_date(x, y)
plt.title("Landsat 7 NDVI time-series Uxmal")
plt.ylabel("NDVI (-)")
plt.grid(True)
plt.show()