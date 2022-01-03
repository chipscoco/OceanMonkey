from oceanmonkey.core.queue import QueueType

class Queue:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, settings):
        self.__settings = settings

    def has(self, queue_type=QueueType.SEEDS):
        settings = self.__settings
        queues = 0
        if queue_type == QueueType.SEEDS:
            if hasattr(settings, "SEEDS_KEY") and hasattr(settings, "SEEDS_QUEUE"):
                queues = len(settings.SEEDS_QUEUE.get(settings.SEEDS_KEY, []))
        elif queue_type == QueueType.SOURCE:
            if hasattr(settings, "SOURCE_KEY") and hasattr(settings, "SOURCE_QUEUE"):
                queues = len(settings.SOURCE_QUEUE.get(settings.SOURCE_KEY, []))
        return queues


    def get(self, queue_type=QueueType.SEEDS):
        settings = self.__settings
        params = {}
        if queue_type == QueueType.SEEDS:
            if hasattr(settings, "SEEDS_KEY") and hasattr(settings, "SEEDS_QUEUE"):
                params = settings.SEEDS_QUEUE[settings.SEEDS_KEY]
        elif queue_type == QueueType.SOURCE:
            if hasattr(settings, "SOURCE_KEY") and hasattr(settings, "SOURCE_QUEUE"):
                params = settings.SOURCE_QUEUE[settings.SOURCE_KEY]
        return params
