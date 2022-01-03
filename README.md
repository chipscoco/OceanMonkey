<img src="https://github.com/chipscoco/OceanMonkey/blob/main/artwork/logo.jpg">
   

Overview
========

OceanMonkey is a High-Level Distributed Web Crawling and Web Scraping framework, used to
crawl websites and extract structured data from their pages. It can be used for
a wide range of purposes, from data mining to monitoring and automated testing.

OceanMonkey was brought to life and is maintained by chenzhengqiang(wechat:Pretty-Style, blog:http://www.chipscoco.com) while teaching the python's web scraping in GuangZhou.

Requirements
============

* Python 3.5+
* Works on Linux, Windows, macOS, BSD

Install
=======

The quick way to install **OceanMonkey**

    pip install oceanmonkey

Quick start
=============
Firstly execute **monkeys startproject** in command line to create a OceanMonkey Project like the following:

    monkeys startproject BeBe
Then write your crawl logic in gibbons.py under the monkeys' directory, and write the store logic in orangutans.py.

Execute the **monkeys run** command under the project's directory finally when you finish your coding work:

    cd BeBe
    monkeys run
    
## Sample code of parsing the page source

```
from oceanmonkey import Gibbon
from oceanmonkey import Request


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
            item['publish_date'] = response.xpath('//span[@class="mr20 waphide"]/text()').extract_first()
            yield item
            self.start_id += 1
            next_url = "http://www.chipscoco.com/?id={}".format(self.start_id)
            yield Request(url=next_url, callback=self.parse)
```

## Contact

|Author          | Email            | Wechat      |
| ---------------|:----------------:| -----------:|
| chenzhengqiang | chenzhengqiang@chipscoco.com | Pretty-Style |

**Notice:  Any comments and suggestions are welcomed**
