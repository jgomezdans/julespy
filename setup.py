from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='julespy',
      version=version,
      description="A python driver to run the JULES model.",
      long_description="""\
This code is a wrapper to the JULES land surface model. The main aims is to have easy access to parameters, drivers and model output from python.""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Jose Gomez-Dans and Martin de Kauwe',
      author_email='j.gomez-dans@geog.ucl.ac.uk',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
