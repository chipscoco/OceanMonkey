<img src="https://github.com/chipscoco/OceanMonkey/blob/main/artwork/logo.jpg">
   

Overview
========

OceanMonkey is a High-Level Distributed Web Crawling and Web Scraping framework base on multi-process and multi-coroutines, used to
crawl websites and extract structured data from their pages like the classical scrapy framework.

## Installation guide

### Supported Python versions

OceanMonkey requires Python 3.5+, either the CPython implementation.

### Installing
if you’re already familiar with installation of Python packages, you can install OceanMonkey and its dependencies from PyPI with:

    pip install oceanmonkey

Also you can install OceanMonkey by dowloading the project's source code and install it through the setup.py:
    
    python setup.py install

## Quick Start

### Create a Monkey Project
use the monkeys command to create a OceanMonkey Project like the following:
  
    monkeys startproject BeBe
or:

    monkeys strtproject  D:\BeBe
    
### Write the scraping logic
when you execute the startproject command, it will generates two Python script file under the monkeys' directory,
namely **gibbons.py** and **orangutans.py**. just write the gibbons.py for scraping.

### Write the store logic
just write the **orangutans.py** for clening and storing items extracted from page source.

### Run the project
it's so easy to run the project, just execute the run command under the project's directory.

    cd BeBe
    monkeys run
    
# Sample code 
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
            yield Signal(value=SignalValue.SAY_GOODBYE)
```
detailed usage on OceanMonkey see [https://github.com/chipscoco/OceanMonkey/tree/main/docs](https://github.com/chipscoco/OceanMonkey/tree/main/docss)

## Contact

|Author          | Email            | Wechat      |
| ---------------|:----------------:| -----------:|
| chenzhengqiang | chenzhengqiang@chipscoco.com | Pretty-Style |

**Notice:  Any comments and suggestions are welcomed**
