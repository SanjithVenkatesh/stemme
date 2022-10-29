"""
setup.py

Metadata necessary for creating pip package

Original Author: Sanjith Venkatesh
Last Modified: October 28, 2022
"""

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()


setup(
    name='stemme',
    version='0.1.0',
    description='Various voting methods',
    long_description=readme,
    author='Sanjith Venkatesh',
    author_email='sanjithv@vivaldi.net',
    url='https://github.com/SanjithVenkatesh/stemme',
    packages=find_packages(exclude=('tests', 'docs'))
)