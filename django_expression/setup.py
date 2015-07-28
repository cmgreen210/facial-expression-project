import os
from setuptools import setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django_expression',
    version='0.1',
    packages=['django_expression'],
    author='Chris Green',
    author_email='cmgreen210@gmail.com',
)