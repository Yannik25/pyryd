#!/usr/bin/env python
# -*- coding: utf-8 -*-

import warnings

try:
    from .pyryd import Ryd
except ImportError as e:
    warnings.warn(ImportWarning(e))

VERSION = (0, 1, 2)

__version__ = '.'.join([str(i) for i in VERSION])
__author__ = 'Yannik25'
__author_email__ = 'yannik92@me.com'
__copyright__ = 'Copyright (C) 2021 Yannik25'
__license__ = "MIT"
__url__ = "https://github.com/Yannik25/pyryd"
