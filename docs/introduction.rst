Introduction
------------


``geextract`` is a python library (API + command lines) to extract Landsat time-series from the Google Earth Engine platform. It can query single pixels or spatially aggregated values over polygons. When used via the command line, extracted time-series are written to a sqlite database.

The idea is to provide quick access to Landsat time-series for exploratory analysis or algorithm testing. Instead of downloading the whole stack of Landsat scenes, preparing the data locally and extracting the time-series of interest, which may take several days, ``geextract`` allows to get time-series in a few seconds.

Compatible with python 2.7 and 3.

This online documentation includes an installation guide, API and command line documentation and some usage examples.