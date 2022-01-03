"""
Queue is the core class that  responsible for transferring url seeds and page source.
"""


import abc
from oceanmonkey.core import database
from oceanmonkey.utils import current_frame
from oceanmonkey.utils import bye
from oceanmonkey.core.database import RedisDataType



class Queue(abc.ABC):
    @abc.abstractmethod
    def get(self, **kwargs):
        """ nothing to do, just  in a daze """

    @abc.abstractmethod
    def put(self, value, **kwargs):
        """ nothing to do, just  in a daze """


class SeedsQueue(Queue):
    def __init__(self, db):
        self.__db = db

    def get(self, **kwargs):
        keys = kwargs["keys"] if "keys" in kwargs else None
        if not keys:
            bye.bye("You must specify the queue's seeds key, check the settings.py carefully!",
                    fn=__name__, lno=current_frame().f_lineno)
        seed, timeout = self.__db.query(**kwargs)
        return seed, timeout

    def put(self, value, **kwargs):
        keys = kwargs["keys"] if "keys" in kwargs else None
        if not keys:
            bye.bye("You must specify the queue's seeds key, check the settings.py carefully!",
                    fn=__name__, lno=current_frame().f_lineno)
        if "data_type" not in kwargs:
            kwargs["data_type"] = RedisDataType.LIST
        return self.__db.add(value, **kwargs)

    @property
    def server(self):
        return self.__db

    def info(self):
        return self.__db.info


class SourceQueue(Queue):
    def __init__(self, db):
        self.__db = db

    def get(self, **kwargs):
        keys = kwargs["keys"] if "keys" in kwargs else None
        if not keys:
            bye.bye("You must specify the queue's source key, check the settings.py carefully!",
                    fn=__name__, lno=current_frame().f_lineno)
        source, timeout = self.__db.query(**kwargs)
        return source, timeout

    def put(self, value, **kwargs):
        keys = kwargs["keys"] if "keys" in kwargs else None
        if not keys:
            bye.bye("You must specify the queue's source key, check the settings.py carefully!",
                    fn=__name__, lno=current_frame().f_lineno)
        if "data_type" not in kwargs:
            kwargs["data_type"] = RedisDataType.SET
        return self.__db.add(value, **kwargs)

    @property
    def server(self):
        return self.__db

    def info(self):
        return self.__db.info


class QueueType:
    SEEDS = 0
    SOURCE = 1


class SimpleQueueFactory:
    __queues = {
        QueueType.SEEDS: SeedsQueue,
        QueueType.SOURCE: SourceQueue,
    }

    @classmethod
    def get_queue(cls, settings, queue_type=QueueType.SEEDS, db_type=database.DatabaseType.REDIS):
        db = database.Database.get_instance(settings, db_type)
        return cls.__queues[queue_type](db) if queue_type in cls.__queues else None

    @classmethod
    def get_queues(cls, settings, queue_type=QueueType.SEEDS, db_type=database.DatabaseType.REDIS_MULTI):
        queues = [1]
        from oceanmonkey.utils.settings import SimpleSettingsFactory
        from oceanmonkey.utils.settings import SettingsType
        settings_factory = SimpleSettingsFactory(settings)
        queue_settings = settings_factory.get(SettingsType.QUEUE)
        params = queue_settings.get(queue_type)

        if params:
            dbs = database.Database.get_instances(settings, params, db_type)
            for db in dbs:
                queues.append(cls.__queues[queue_type](db) if queue_type in cls.__queues else None)
        return queues
