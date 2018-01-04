#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
from setuptools import setup, find_packages
import itertools

# Parse the version from the geextract module.
with open('geextract/__init__.py') as f:
    for line in f:
        if line.find("__version__") >= 0:
            version = line.split("=")[1].strip()
            version = version.strip('"')
            version = version.strip("'")
            continue

# 
extra_reqs = {'docs': ['sphinx',
                       'sphinx-rtd-theme',
                       'sphinxcontrib-programoutput',
                       'fiona',
                       'seaborn',
                       'matplotlib']}
extra_reqs['all'] = list(set(itertools.chain(*extra_reqs.values())))

with codecs.open('README.rst', encoding='utf-8') as f:
    readme = f.read()

setup(name='geextract',
      version=version,
      description=u"Extract Landsat surface reflectance time-series at given location from google earth engine",
      long_description=readme,
      classifiers=[],
      keywords='Landsat, surface reflectance, google, gee, time-series',
      author=u"Loïc Dutrieux",
      author_email='loic.dutrieux@gmail.com',
      url='https://github.com/loicdtx/landsat-extract-gee.git',
      license='GPLv3',
      packages=find_packages(),
      install_requires=[
          'pandas',
          'earthengine-api'],
      scripts=['geextract/scripts/gee_extract.py',
               'geextract/scripts/gee_extract_batch.py'],
      test_suite="tests",
      extras_require=extra_reqs)
