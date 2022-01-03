"""
just logging error message and say goodbye.
"""

import logging
from oceanmonkey.utils.log import logger

import sys


def bye(error, fn, lno, *args):
    record = logger.makeRecord(logger.name, logging.ERROR,
                               fn, lno, error, args, exc_info=None)
    logger.handle(record)
    sys.exit()
