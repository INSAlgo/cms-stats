"""
cms-stats provides an API to retrieve and fetch
data exported from a CMS database, using psycopg2 and matplotlib

Copyright 2020, Louis Gombert
Licensed under AGPL-3.0 license
"""
from setuptools import setup

setup(name='cms-stats',
      version='0.1',
      description='Python API to export aggregated data from a CMS contest database',
      author='Louis Gombert',
      license='AGPL-3.0',
      packages=['cms-stats'],
      zip_safe=False)
