"""
OceanMonkey - A lightweight distributed web crawling and web scraping framework written for Python
"""

import pkgutil
import sys
import warnings


# Declare top-level shortcuts
from oceanmonkey.core.monkey import Macaque, Gibbon, Orangutan
from oceanmonkey.core.request import Request
from oceanmonkey.core.response import Response
from oceanmonkey.core.signal import Signal
from oceanmonkey.core.signal import SignalValue


__all__ = [
    '__version__', 'version_info', 'Macaque', 'Gibbon', 'Orangutan',
    'Request', 'Response', 'Signal', 'SignalValue'
]


# OceanMonkey's version
__version__ = (pkgutil.get_data(__package__, "VERSION") or b"").decode("ascii").strip()
version_info = tuple(int(v) if v.isdigit() else v for v in __version__.split('.'))


# Check minimum required Python version
if sys.version_info < (3, 5):
    print("Scrapy %s requires Python 3.5+" % __version__)
    sys.exit(1)


del pkgutil
del sys
del warnings
