
class Deploy:
    __instance = None
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, settings):
        self.__settings = settings

    def get(self):
        return self.__settings.MONKEYS_DEPLOY_MODE \
        if hasattr(self.__settings, "MONKEYS_DEPLOY_MODE") else 0

