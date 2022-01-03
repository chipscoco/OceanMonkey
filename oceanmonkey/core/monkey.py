"""
Monkey is the class which breeding monkeys to be a crawler.
Three kinds of monkey like the following:
(1) Macaque play the role of downloader.
(2) Gibbon play the role of  analyzer.
(3) Orangutan that play the role of  porter that load data into database.
"""


import abc


class Macaque(abc.ABC):
    @abc.abstractmethod
    def on_request(self, request):
        """ Macaque play the role of downloader """


class Gibbon(abc.ABC):
    @abc.abstractmethod
    def parse(self, response):
        """ Gibbon play the role of  analyzer """


class Orangutan(abc.ABC):
    @abc.abstractmethod
    def process_item(self, item):
        """ Orangutan that play the role of  porter """


class MonkeyType:
    MACAQUE = 0
    GIBBON = 1
    ORANGUTAN = 2


