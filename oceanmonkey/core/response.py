"""
This is the Core Response Class.
"""

from parsel import Selector


class Response:
    def __init__(self, url, page_source,
                 status_code=200,
                 headers = {},
                 meta=None,
                 callback=None,
                 repeated=False):

        self.__url = url
        self.__page_source = page_source
        self.__selector = Selector(self.__page_source)
        self.__status_code = status_code
        self.__headers = headers
        self.__meta = meta
        self.__callback = callback
        self.__repeated = repeated

    @property
    def url(self):
        return self.__url

    @property
    def page_source(self):
        return self.__page_source

    @property
    def status_code(self):
        return self.__status_code

    @property
    def meta(self):
        return self.__meta

    @meta.setter
    def meta(self, meta_):
        self.__meta = meta_

    @property
    def headers(self):
        return self.__headers

    @headers.setter
    def headers(self, headers_):
        self.__headers.update(headers_)

    @property
    def callback(self):
        return self.__callback

    @property
    def repeated(self):
        return self.__repeated

    @repeated.setter
    def repeated(self, true_or_false):
        self.__repeated = true_or_false

    @callback.setter
    def callback(self, callback_):
        self.__callback = callback_

    def maybe_bad_status(self):
        return True if self.__status_code == 200 else False

    def get_init_args(self, include_page_source=True):
        init_args = {
                "url": self.__url,
                "page_source": self.__page_source,
                "status_code": self.__status_code,
                "meta": self.__meta,
                "callback": self.__callback,
                "repeated": self.__repeated
        }
        if include_page_source:
            init_args["page_source"] = self.__page_source
        return init_args

    def parse(self, response):
        return self.__callback(response)

    def xpath(self, query, namespace=None, **kwargs):
        return self.__selector.xpath(query, namespace, **kwargs)

    def re(self, regex, replace_entitles=True):
        return self.__selector.re(regex, replace_entitles)

    def css(self, query):
        return self.__selector.css(query)
