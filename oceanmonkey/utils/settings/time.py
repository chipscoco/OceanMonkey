class TimeType:
    DELAY = 0
    IDLE = 1

class Time:
    __instance = None
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, settings):
        self.__settings = settings

    def get(self, time_type=TimeType.IDLE):
        settings = self.__settings
        value = None
        if time_type == TimeType.IDLE:
            value = settings.MAX_IDLE_TIME if hasattr(settings, "MAX_IDLE_TIME") else None
        elif time_type == TimeType.DELAY:
            value = settings. CRAWLING_DELAY if hasattr(settings, " CRAWLING_DELAY") else 0
            value = value / 1000 if value > 0 else 0
        return value
