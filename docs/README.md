<img src="https://github.com/chipscoco/OceanMonkey/blob/main/artwork/logo.jpg">

# OceanMonkey 1.0 documentation
ceanMonkey is a High-Level Distributed Web Crawling and Web Scraping framework base on multi-process and multi-coroutines, used to
crawl websites and extract structured data from their pages like the classical scrapy framework.

## Installation guide

### Supported OS

    OceanMonkey works on Linux, Windows and macOS.

### Supported Python versions

    OceanMonkey requires Python 3.5+, either the CPython implementation.

### Installing
if you’re already familiar with installation of Python packages, you can install OceanMonkey and its dependencies from PyPI with:

    pip install oceanmonkey

Also you can install OceanMonkey by dowloading the project's source code and install it through the setup.py:
    
    python setup.py install

## Development guide

### Create a Monkey Project
use the monkeys command to create a OceanMonkey Project like the following:
  
    monkeys startproject BeBe
or:

    monkeys strtproject  D:\BeBe
### Configure the settings.py

there are three kinds of monkey like the following:
    
    - Macaque play the role of downloader.
    - Gibbon play the role of analyzer.
    - Orangutan play the role of porter.
one monkey one process, so if you want configure multi-process just modify the global MONKEYS variable in settings.py like the following:

```
MONKEYS = {
    # sent monkeys to download or analyze by changing the value
    # e.g.:{"MACAQUE": 5,}, it means to construct 5 macaques for downloading
    MACAQUE: 1,
    GIBBON: 1,
}
```
and you must configure the SEEDS_QUEUE and SOURCE_QUEUE for the sake of distributed support:
```
# Configure the  Seeds Queue by OceanMonkey (default: Redis's set)
SEEDS_KEY = "ocean_seeds"
SEEDS_QUEUE = {
    # key represent the redis's set key
    SEEDS_KEY: [
        {"host": "localhost", "port": 6379, "password": "your redis password"},
    ]
}


# Configure the Page Source Queue by OceanMonkey (default: Redis's set)
SOURCE_KEY = "ocean_source"
SOURCE_QUEUE = {
    # key represent the redis's set key
    SOURCE_KEY: [
        {"host": "localhost", "port": 6379, "password": "your redis password"},
    ]
}
```

### Write the scraping logic
when you execute the startproject command, it will generates two Python script file under the monkeys' directory,
namely gibbons.py and orangutans.py. just write the gibbons.py for scraping.

### Write the store logic
just write the orangutans.py for clening and storing items extracted from page source.



### Run the project
it's so easy to run the project, just execute the run command under the project's directory.

    cd BeBe
    monkeys run
