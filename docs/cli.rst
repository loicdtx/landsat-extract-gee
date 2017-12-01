Command line interface
----------------------

ggextract comes with two Command Line Interfaces for convenience. Both CLI expose the functionalities of `geextract.ts_extract()` function, to extract a time-series from a single pixel or a circular buffer. The `gee_extract_batch` command takes a text file as input in which coordinates and name of multiple locations may be written, allowing batch ordrering of data. Both CLI write the extracted data to a sqlite database.


Simple CLI for ordering a single time-series and write it to a sqlite database
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. program-output:: gee_extract.py --help


Batch ordering CLI
^^^^^^^^^^^^^^^^^^

.. program-output:: gee_extract_batch.py --help