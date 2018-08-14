Processing
----------

Data sources
^^^^^^^^^^^^

For now ``geextract`` only supports the extraction of Landsat surface reflectance data. Two Landsat surface reflectance collections are available on the platform; pre-collection and collection 1. It is preferable to use collection 1 as it is supposedly of better quality (more recent version of ledaps and cloud masking algorithm) and is more up to date (pre-collection data are no longer ingested on the google earth engine platform so that recent data won't be available).
Reference documents (product guides) for Landsat surface reflectance data are available `here <https://landsat.usgs.gov/sites/default/files/documents/ledaps_product_guide.pdf>`_ for Landsat 4, 5 and 7, and `here <https://landsat.usgs.gov/sites/default/files/documents/lasrc_product_guide.pdf>`_ for Landsat 8.

Pre-processing
^^^^^^^^^^^^^^

A rather standard pre-processing consisting of cloud and cloud shadow masking and removal of saturated pixels is applied to the data prior to extraction.

The cfmask quality data (available in the cfmask band for pre-collection and pixel_qa for collection 1) are used for masking pixels contaminated by clouds, cloud shadows or being water, ice, etc... This is done by keeping only pixels labeled as "clear land pixel".

Saturated pixels are filtered out by excluding out of valid range values. 

Spatial aggregation methods
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The user can either order time-series corresponding to a single pixel or a polygon. When a polygon is used, one of the four spatial aggregation functions (mean, median, max. min) can be chosen. Masked pixels are automatically excluded from the spatial aggregation.