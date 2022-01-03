"""
This is the Core Request Class.
"""

import aiohttp


class Request:
    def __init__(self, url, method="GET", body=None,
                 meta=None, callback=None, refuse_filter=False):
        self.__url = url
        self.__meta = meta
        self.__method = method
        self.__body = body
        self.__headers = {}
        self.__callback = callback
        self.__refuse_filter = refuse_filter

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, url_):
        self.__url = url_

    @property
    def body(self):
        return self.__body

    @property
    def meta(self):
        return self.__meta

    @property
    def callback(self):
        return self.__callback

    @property
    def refuse_filter(self):
        return self.__refuse_filter

    @property
    def method(self):
        return self.__method

    def add_headers(self, headers):
        self.__headers.update(headers)

    @property
    def headers(self):
        return self.__headers

    @headers.setter
    def headers(self, headers_):
        self.__headers.update(headers_)

    async def do_request(self):
        if self.__method.upper() == "GET":
            async with aiohttp.ClientSession(headers=self.__headers) as session:
                async with session.get(self.__url) as resp:
                    page_source = await resp.text()
                    return self.__url, page_source, resp.status
        return self.__url, None, None
