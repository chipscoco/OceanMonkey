"""
This module contains the default values for all settings used by OceanMonkey.
"""


"""
Three kinds of monkey like the following:
(1) Macaque play the role of downloader.
(2) Gibbon play the role of  analyzer.
(3) Orangutan play the role of  porter.
"""
MACAQUE = 0
GIBBON = 1
ORANGUTAN = 2

MONKEYS = {
    # sent monkeys to download or analyze by change the value
    # e.g.:{"MACAQUE": 5,}, it means to construct 5 macaques for downloading
    MACAQUE: 1,
    GIBBON: 1,
}


"""
0 represents the local mode, each monkey do their own task in a single machine.
if there is only macaque in a machine, then all tasks will be transferred to macaque. 
1 represents the distributed mode, each monkey do their own task in a distributed network.
"""
MONKEYS_DEPLOY_MODE = 1
GIBBONS_MODULES = ['monkeys.gibbons', ]
ORANGUTANS_MODULES = ['monkeys.orangutans', ]

# Database
DATABASES = {
    "mysql": {
        "host": "localhost",
        "username": "xxx",
        "password": "xxx",
        "name": "",
    },
}


# Configure the  Seeds Queue by OceanMonkey (default: Redis's set)
SEEDS_KEY = "ocean_seeds"
SEEDS_QUEUE = {
    # key represent the redis's set key
    SEEDS_KEY: [
        {"host": "localhost", "port": 6379, },
    ]
}


# Configure the  Page Source Queue by OceanMonkey (default: Redis's set)
SOURCE_KEY = "ocean_source"
SOURCE_QUEUE = {
    # key represent the redis's set key
    SOURCE_KEY: [
        {"host": "localhost", "port": 6379, },
    ]
}

MACAQUE_MIDDLEWARES = [
    "monkeys.middlewares.RandomUserAgentMiddleware",
]


CRAWLING_DELAY = 2
# Waiting for seed from producer process, default 10 milliseconds
QUEUE_TIMEOUT = 10
DOWNLOADING_COROUTINES = 8
# Ocean Monkey closed when monkey's free seconds greater than the max idle time
MAX_IDLE_TIME = 120

# Config the logging's level here
# 10-->DEBUG 20-->INFO, 30-->WARNING...and so on
LOGGING_LEVEL = 20
# Config the logging's format here
# LOGGING_FORMAT = '%(asctime)s %(levelname)s [%(filename)s:%(lineno)d]-- %(message)s'

# Override the default request headers here:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'zh-cn',
#}

