Processing
----------

Data sources
^^^^^^^^^^^^

Landsat surface reflectance:
	- (reference to usgs pdfs)
	- pre-collection. Description
	- collection 1. Description
	  
Data preparation steps:
	- geextract applies a standard pre-processing to the data
	- Masking of non clear land pixels (cloud, shadows, water, snow, ...)
	- Masking of saturated pixels
	- Neither included in results (when querying single pixels), nor used when computing spatial aggregation metrics (order placed for an area)
	- When ordering an area (polygon feature or point + buffer), 4 spatial aggregation methods are available