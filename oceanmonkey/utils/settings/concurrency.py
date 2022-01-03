class Concurrency:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, settings):
        self.__settings = settings

    def get(self):
        queue_timeout = self.__settings.QUEUE_TIMEOUT / 1000 if hasattr(self.__settings, "QUEUE_TIMEOUT") else 0.01
        queue_timeout = 0.01 if queue_timeout <0 else queue_timeout
        max_seeds_size = self.__settings.MAX_SEEDS_SIZE if hasattr(self.__settings, "MAX_SEEDS_SIZE") else 8
        max_seeds_size = 1 if max_seeds_size <=0 else max_seeds_size
        max_buffer_time = self.__settings.MAX_BUFFER_TIME /1000 if hasattr(self.__settings, "MAX_BUFFER_TIME") else 0.2
        max_buffer_time = 0.2 if max_buffer_time < 0 else max_buffer_time
        return queue_timeout, max_seeds_size, max_buffer_time
