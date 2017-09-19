

## Installation

In vitual environment

```
pip install git+https://github.com/loicdtx/landsat-extract-gee.git
```

If you're using the gee API for the first time on your machine, you'll have to run:

```
earthengine authenticate
```

which will open a google authentication page in your browser, and will give you an authentication token to paste back in the terminal.

You can check that the authentication process was successful by running.

```
python -c "import ee; ee.Initialize()"
```

If nothing happens... it's working.

## Benchmark

A quick benchmark of the extraction speed, using a 500 m buffer.

```python
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

# 'LT5. Extracted 142 records in 1.9 seconds'
# 'LE7. Extracted 249 records in 5.8 seconds'
# 'LT4. Extracted 7 records in 1.0 seconds'
# 'LC8. Extracted 72 records in 2.4 seconds'
```
