from oceanmonkey.core.filters import RequestDupFilter, PageSourceDupFilter
from oceanmonkey.core.monkey import MonkeyType

class FilterType:
    REQUEST_FILTER = 0
    SOURCE_FILTER = 1

class Filters:
    __instance = None
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, settings):
        self.__settings = settings

    def get(self, filter_type=FilterType.REQUEST_FILTER):
        settings = self.__settings
        dup_filter = None
        filters = settings.MONKEY_DUP_FILTERS if hasattr(settings, "MONKEY_DUP_FILTERS") else None
        if filter_type == FilterType.REQUEST_FILTER:
            if filters and MonkeyType.MACAQUE in filters:
                filter_module = importlib.import_module(filters[MonkeyType.MACAQUE])
                dup_filter = filter_module()
            else:
                dup_filter = RequestDupFilter()
        elif filter_type == FilterType.SOURCE_FILTER:
            if filters and MonkeyType.GIBBON in filters:
                filter_module = importlib.import_module(filters[MonkeyType.GIBBON])
                dup_filter = filter_module()
            else:
                dup_filter = PageSourceDupFilter()
        return dup_filter
