"""
This is the Core Database class
"""

import MySQLdb
import redis

from oceanmonkey.utils import current_frame
from oceanmonkey.utils import bye
from oceanmonkey.utils.log import logger


class DatabaseType:
    MYSQL = 0
    REDIS = 1
    REDIS_MULTI = 2


class RedisDataType:
    LIST = 0
    SET = 1


class Database:
    __db_instances = {}

    @classmethod
    def get_instance(cls, settings, db_type=DatabaseType.MYSQL):
        """
        :param settings: the project's settings
        :param db_type: the database type, default MySQL
        :return: the singleton of database
        """
        if db_type not in cls.__db_instances:
            cls.__db_instances[db_type] = Database(settings, db_type)
        return cls.__db_instances[db_type]

    @classmethod
    def get_instances(cls, settings, params, db_type=DatabaseType.REDIS_MULTI):
        """
        :param settings: the project's settings
        :param params:a list of database's connection param,e.g:[{"host": "xx", "port": 6379, "password": "xx",}]
        :param db_type: default multi redis
        :return: multi singleton of database
        """
        if db_type not in cls.__db_instances:
            cls.__db_instances[db_type] = [Database(settings, db_type, **param) for param in params]
        return cls.__db_instances[db_type]

    def __init__(self, settings, db_type=DatabaseType.MYSQL, **kwargs):
        self.__settings = settings
        self.__db_type = db_type
        self.__db_config = {}
        self.__db = self.__get_database(**kwargs)
        self.__cursors = {}
        self.__db_info = self.__get_database_information()

    def __get_database(self, **kwargs):
        db = None
        settings = self.__settings
        config = settings.DATABASES if not kwargs else kwargs
        if self.__db_type == DatabaseType.MYSQL:
            self.__db_config = config["mysql"] if "mysql" in config else  config
            try:
                port = self.__db_config["port"] if "port" in self.__db_config else 3306
                charset = self.__db_config["charset"] if "charset" in self.__db_config else "utf8"
                db = MySQLdb.connect(host=self.__db_config["host"],
                                     user=self.__db_config["username"],
                                     password=self.__db_config["password"],
                                     db=self.__db_config["name"],
                                     port=port,
                                     charset=charset
                                     )
            except (Exception, ) as e:
                bye.bye(e, fn=__name__, lno=current_frame().f_lineno)

        elif self.__db_type in {DatabaseType.REDIS, DatabaseType.REDIS_MULTI}:
            self.__db_config = config["redis"] if "redis" in config else config
            try:
                host = self.__db_config["host"] if "host" in self.__db_config else "localhost"
                port = self.__db_config["port"] if "port" in self.__db_config else 6379
                password = self.__db_config["password"] if "password" in self.__db_config else ""
                params = {"host": host, "port": port}
                if password:
                    params["password"] = password
                db = redis.Redis(**params, socket_connect_timeout=2)
                db.ping()
            except (Exception, ) as e:
                bye.bye(e, fn=__name__, lno=current_frame().f_lineno)

        return db

    def add(self, value, **kwargs):
        ok = True
        if self.__db_type in {DatabaseType.REDIS, DatabaseType.REDIS_MULTI}:
            data_type = kwargs["data_type"] if "data_type" in kwargs else None
            keys = kwargs["keys"] if "keys" in kwargs else None

            if data_type == RedisDataType.LIST:
                try:
                    self.__db.lpush(keys, value)
                except (Exception, ) as e:
                    ok = False
                    logger.error(e)
            elif data_type == RedisDataType.SET:
                try:
                    self.__db.sadd(keys, value)
                except (Exception, ) as e:
                    ok = False
                    logger.error(e)
        return ok

    def query(self, **kwargs):
        value = None
        is_timeout = False
        if self.__db_type in {DatabaseType.REDIS, DatabaseType.REDIS_MULTI}:
            timeout = kwargs["timeout"] if "timeout" in kwargs else None
            if timeout == 0:
                timeout = -1
            try:
                value = self.__db.brpop(kwargs["keys"], timeout=timeout)
                if value is None:
                    is_timeout = True
                value = value[1] if value else b""
            except (Exception, ):
                is_timeout = True
        return value, is_timeout

    def exists(self, **kwargs):
        ret = True
        if self.__db_type in {DatabaseType.REDIS, DatabaseType.REDIS_MULTI}:
            name = kwargs["name"]
            value = kwargs["value"]
            if not self.__db.sismember(name, value):
                ret = False
        return ret

    def __get_database_information(self):
        info = {"database": "unknown"}
        if self.__db_type == DatabaseType.MYSQL:
            info["database"] = "MySQL"
        elif self.__db_type in {DatabaseType.REDIS, DatabaseType.REDIS_MULTI}:
            info["database"] = "Redis"
        info["host"] = self.__db_config["host"] if "host" in self.__db_config else "unknown"
        info["port"] = self.__db_config["port"] if "port" in self.__db_config else "unknown"
        return info

    @property
    def info(self):
        return self.__db_info
