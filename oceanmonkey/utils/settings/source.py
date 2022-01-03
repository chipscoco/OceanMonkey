class Source:
    __instance = None
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, settings):
        self.__settings = settings


    def get(self):
        settings = self.__settings
        return settings.SOURCE_KEY if hasattr(settings, "SOURCE_KEY") else None
