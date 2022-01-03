from oceanmonkey.utils.settings.concurrency import Concurrency
from oceanmonkey.utils.settings.deploy import Deploy
from oceanmonkey.utils.settings.filters import Filters
from oceanmonkey.utils.settings.headers import Headers
from oceanmonkey.utils.settings.middleware import Middleware
from oceanmonkey.utils.settings.monkey import Monkey
from oceanmonkey.utils.settings.queue import Queue
from oceanmonkey.utils.settings.seeds import Seeds
from oceanmonkey.utils.settings.source import Source
from oceanmonkey.utils.settings.time import Time

class SettingsType:
    CONCURRENCY = 0
    DEPLOY = 1
    FILTERS = 2
    HEADERS = 3
    MIDDLEWARE = 4
    MONKEY = 5
    QUEUE = 6
    SEEDS = 7
    SOURCE = 8
    TIME = 9

SettingsClass = {
    SettingsType.CONCURRENCY: Concurrency,
    SettingsType.DEPLOY: Deploy,
    SettingsType.HEADERS: Headers,
    SettingsType.MIDDLEWARE: Middleware,
    SettingsType.MONKEY: Monkey,
    SettingsType.QUEUE: Queue,
    SettingsType.SEEDS: Seeds,
    SettingsType.SOURCE: Source,
    SettingsType.TIME: Time,
    SettingsType.FILTERS: Filters
}


class SimpleSettingsFactory:
    __instance = None
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, settings):
        self.__settings = settings

    def get(self, settings_type):
        return SettingsClass[settings_type](self.__settings) \
            if settings_type in SettingsClass else None
