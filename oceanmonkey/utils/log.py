"""
if you want  to record log in file, just import the log.logger.
"""


import logging
from oceanmonkey.settings import default_settings as settings

LOGGING_LEVELS = {
    10: logging.DEBUG,
    20: logging.INFO,
    30: logging.WARNING,
    40: logging.ERROR,
    50: logging.CRITICAL
}

logging_basic_config = {}
if hasattr(settings, "LOGGING_LEVEL" ):
    logging_basic_config["level"] = LOGGING_LEVELS[settings.LOGGING_LEVEL]
else:
    logging_basic_config["level"] = logging.WARNING

if hasattr(settings, "LOGGING_FORMAT" ):
    logging_basic_config["format"] = logging.LOGGING_FORMAT
else:
    logging_basic_config["format"] = '%(asctime)s %(levelname)s [%(filename)s:%(lineno)d]  %(message)s'


logging.basicConfig(**logging_basic_config)
logger = logging.getLogger()