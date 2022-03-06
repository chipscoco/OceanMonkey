<img src="https://github.com/chipscoco/OceanMonkey/blob/main/artwork/logo.jpg">

# OceanMonkey 1.0 documentation
OceanMonkey is a High-Level Distributed Web Crawling and Web Scraping framework base on multi-process and multi-coroutines, used to
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
and you must configure the **SEEDS_QUEUE** and **SOURCE_QUEUE** for the sake of distributed support:
```
# Configure the  Seeds Queue by OceanMonkey (default: Redis's set)
SEEDS_KEY = "ocean_seeds"
SEEDS_QUEUE = {
    # key represents the redis's set key
    SEEDS_KEY: [
        {"host": "localhost", "port": 6379, "password": "your redis password"},
    ]
}


# Configure the Page Source Queue by OceanMonkey (default: Redis's set)
SOURCE_KEY = "ocean_source"
SOURCE_QUEUE = {
    # key represents the redis's set key
    SOURCE_KEY: [
        {"host": "localhost", "port": 6379, "password": "your redis password"},
    ]
}
```
override the default macaque's downloading behavior, you must provide a download middlware written in middlewares.py
through the global variable **MACAQUE_MIDDLEWARES**:

```
# Configure the macaque middleware class for downloading
MACAQUE_MIDDLEWARES = [
    "BeBe.middlewares.RandomUserAgentMiddleware",
]
```

## Here are a example about how to write a macaque middleware:
```
# Define here the models for OceanMonkey's  download middleware

from oceanmonkey import Macaque
from oceanmonkey import Response
import random
import requests

class RandomUserAgentMiddleware(Macaque):
    def __init__(self):
        self.__user_agents = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:58.0) Gecko/20100101 Firefox/58.0"
        ]

    # prepare the http request by overriding prepare method
    def prepare(self, request):
        request.headers['User-Agent'] = random.choice(self.__user_agents)
        return request

    def on_request(self, request):
        resp = requests.get(request.url)
        return Response(url=request.url, page_source=resp.text,
                        headers=resp.headers,
                        status_code=resp.status_code)

    def on_finish(self, response):
        response.headers['monkey'] = 'OceanMonkey'
        return response

```

### Write the scraping logic
when you execute the startproject command, it will generates two Python script file under the monkeys' directory,
namely gibbons.py and orangutans.py. just write the gibbons.py for scraping.

#### Sample code of gibbons.py
```
from oceanmonkey import Gibbon
from oceanmonkey import Request
from oceanmonkey import Signal,SignalValue


class WuKong(Gibbon):
    handle_httpstatus_list = [404, 500]
    allowed_domains = ['www.chipscoco.com']
    start_id = 9

    def parse(self, response):
        if response.status_code in self.handle_httpstatus_list or response.repeated:
            self.start_id += 1
            next_url = "http://www.chipscoco.com/?id={}".format(self.start_id)
            yield Request(url=next_url, callback=self.parse)
        else:
            item = {}
            item['author'] = response.xpath('//span[@class="mr20"]/text()').extract_first()
            item['title'] = response.xpath('//h1[@class="f-22 mb15"]/text()').extract_first()
            yield item
            self.start_id += 1
            next_url = "http://www.chipscoco.com/?id={}".format(self.start_id)
            yield Request(url=next_url, callback=self.parse)
           
```

### Write the store logic
just write the orangutans.py for clening and storing items extracted from page source.


### Run the project
it's so easy to run the project, just execute the run command under the project's directory.

    cd BeBe
    monkeys run
