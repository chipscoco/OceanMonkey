import importlib


class MiddlewareType:
    MACAQUE = 0

class Middleware:
    __instance = None
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, settings):
        self.__settings = settings

    def get(self, middleware_type = MiddlewareType.MACAQUE):
        middlewares = []
        if middleware_type == MiddlewareType.MACAQUE:
            if hasattr(self.__settings, "MACAQUE_MIDDLEWARES"):
                for middleware in self.__settings.MACAQUE_MIDDLEWARES:
                    index = middleware.rfind(".")
                    module = middleware[:index]
                    cls = middleware[index + 1:]
                    module = importlib.import_module(module)
                    middleware_cls = getattr(module, cls)
                    middlewares.append(middleware_cls())
        return middlewares
