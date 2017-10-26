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
extra_reqs = {'docs': ['sphinx', 'sphinx-rtd-theme']}
extra_reqs['all'] = list(set(itertools.chain(*extra_reqs.values())))

setup(name='geextract',
      version=version,
      description=u"Extract Landsat surface reflectance time-series at given location from google earth engine",
      classifiers=[],
      keywords='Landsat, surface reflectance, google, gee, time-series',
      author=u"Loic Dutrieux",
      author_email='loic.dutrieux@gmail.com',
      url='https://github.com/loicdtx/landsat-extract-gee.git',
      license='GPLv3',
      packages=find_packages(),
      install_requires=[
          'pandas',
          'earthengine-api'],
      scripts=['geextract/scripts/gee_extract.py'],
      test_suite="tests",
      extras_require=extra_reqs)
