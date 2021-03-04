#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

import pyryd

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='PyRYD',
    version=pyryd.__version__,
    description='python variant to read data from RYD (previously known as TankTaler) ODB2 Adapter',
    author=pyryd.__author__,
    author_email=pyryd.__author_email__,
    url='https://github.com/Yannik25/pyryd',
    py_modules=['pyryd'],
    packages=find_packages(),
    package_data={'': ['*.html', '*.htm']},
    install_requires=['json', 'requests','uuid'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    license=pyryd.__license__,
    classifiers=[
        'Development Status :: 4 - Beta',
        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Object Brokering',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='python ryd tanktaler home automation car obd adapter',
    python_requires='>=3',
    test_suite='pyryd.tests',
)