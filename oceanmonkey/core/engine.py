"""
This is the OceanMonkey engine which controls all the monkeys to crawling data
"""
import time
import importlib
import multiprocessing
import copy
import pickle
import threading
import asyncio

from threading import Lock, Condition
from oceanmonkey.core.monkey import MonkeyType
from oceanmonkey.core.request import Request
from oceanmonkey.core.response import Response
from oceanmonkey.utils.settings.filters import FilterType
from oceanmonkey.utils.settings.time import TimeType
from oceanmonkey.utils.settings import SettingsType
from oceanmonkey.utils.settings import SimpleSettingsFactory
from oceanmonkey.core.queue import SimpleQueueFactory
from oceanmonkey.core.queue import QueueType
from oceanmonkey.core.signal import SignalValue, Signal
from oceanmonkey.utils import current_frame
from oceanmonkey.utils.url import domain
from oceanmonkey.utils import queues as Queues
from oceanmonkey.utils.log import logger
from oceanmonkey.utils import bye


class OceanMonkey:
    __instance = None
    LOCAL = 0
    CLUSTER = 1

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, settings_path=None):
        self.__monkeys = {
            MonkeyType.MACAQUE: self._consume_seeds,
            MonkeyType.GIBBON: self._consume_sources,
        }
        self.__settings_path = settings_path
        self.__settings = importlib.import_module(settings_path)

        self.__seed_queues = []
        self.__source_queues = []
        self.__macaque_monkeys = []
        self.__gibbon_monkeys = []
        self.__monkey_queues = {}
        self.__seeds_lock = Lock()
        self.__source_lock = Lock()

    @property
    def settings(self):
        return self.__settings

    @staticmethod
    def _receive_a_goodbye_signal(value):
        goodbye = False
        try:
            may_be_signal = pickle.loads(value)
            if isinstance(may_be_signal, (Signal,)) and may_be_signal.value == SignalValue.SAY_GOODBYE:
                goodbye = True
        except (KeyError,):
            pass
        return goodbye

    @staticmethod
    def _is_alive(monkeys):
        is_alive = False
        for monkey in monkeys:
            if monkey.is_alive():
                is_alive = True
                break
        return is_alive

    @staticmethod
    def _produce_seeds(settings_path, seeds_queue, macaque_queues, monkeys, seeds_lock):
        settings = importlib.import_module(settings_path)
        settings_factory = SimpleSettingsFactory(settings)
        monkey_settings = settings_factory.get(SettingsType.MONKEY)
        seeds_settings = settings_factory.get(SettingsType.SEEDS)
        seeds_key = seeds_settings.get()
        macaques = monkey_settings.has(MonkeyType.MACAQUE)
        time_settings = settings_factory.get(SettingsType.TIME)
        max_idle_time = time_settings.get()

        while True:
            logger.info("Getting seed from seeds queue:{}".format(seeds_queue.info()))
            value, timeout = seeds_queue.get(keys=seeds_key, timeout=max_idle_time)
            if timeout:
                logger.info("Macaque for seeds closed because of timeout")
                break
            if not OceanMonkey._is_alive(monkeys):
                seeds_queue.put(value)
                logger.info("Macaque for seeds closed because of there are no monkeys")
                break
            if OceanMonkey._receive_a_goodbye_signal(value):
                logger.info("Macaque for seeds closed because of receiving the goodbye's signal")
                break
            logger.info("Seed produced from seeds queue:{}".format(seeds_queue.info()))
            seeds_lock.acquire() if macaques > 1 else None
            """
            choose the backend's monkey with round robin.
            the first element of monkey_queues indicates the backend monkey queues' index
            e.g.: [1, queue, queue,...]
            """
            macaque_queue = Queues.next_queue(macaque_queues)
            seeds_lock.release() if macaques > 1 else None
            macaque_queue.put(value) if macaque_queue else bye.bye("You must configure at least one macaque",
                                                                   fn=__name__, lno=current_frame().f_lineno)
            logger.info("Transfer seed to macaque monkey".format(value))

    @staticmethod
    def _produce_source(settings_path, source_queue, gibbon_queues, monkeys, source_lock):
        settings = importlib.import_module(settings_path)
        settings_factory = SimpleSettingsFactory(settings)
        monkey_settings = settings_factory.get(SettingsType.MONKEY)
        source_settings = settings_factory.get(SettingsType.SOURCE)
        source_key = source_settings.get()
        gibbons = monkey_settings.has(MonkeyType.GIBBON)
        time_settings = settings_factory.get(SettingsType.TIME)
        max_idle_time = time_settings.get()

        while True:
            logger.info("Getting  source from source queue:{}".format(source_queue.info()))
            value, timeout = source_queue.get(keys=source_key, timeout=max_idle_time)
            if timeout:
                logger.info("Gibbon for source closed because of timeout")
                break
            if not OceanMonkey._is_alive(monkeys):
                source_queue.put(value)
                logger.info("Gibbon for source closed because of there are no monkeys")
                break
            if OceanMonkey._receive_a_goodbye_signal(value):
                logger.info("Gibbon for source closed because of receiving the goodbye's signal")
                break
            logger.info("Source produced from source queue:{}".format(source_queue.info()))
            source_lock.acquire() if gibbons > 1 else None
            """
            choose the backend's monkey with round robin.
            the first element of monkey_queues indicates the backend monkey queues' index
             e.g.: [1, queue, queue, ...]
            """
            gibbon_queue = Queues.next_queue(gibbon_queues)
            source_lock.release() if gibbons > 1 else None
            gibbon_queue.put(value) if gibbon_queue else bye.bye("You must configure at least one gibbon",
                                                                 fn=__name__, lno=current_frame().f_lineno)
            logger.info("Produce page source to gibbon monkey")

    @staticmethod
    def _consume_seeds(settings_path, macaque_queue, gibbon_queues):
        settings = importlib.import_module(settings_path)
        seeds = []

        seeds_waiter = Condition(Lock())
        seed_queues = SimpleQueueFactory.get_queues(settings, QueueType.SEEDS)
        source_queues = SimpleQueueFactory.get_queues(settings, QueueType.SOURCE)

        settings_factory = SimpleSettingsFactory(settings)
        concurrency_settings = settings_factory.get(SettingsType.CONCURRENCY)
        deploy_settings = settings_factory.get(SettingsType.DEPLOY)
        filter_settings = settings_factory.get(SettingsType.FILTERS)

        monkey_settings = settings_factory.get(SettingsType.MONKEY)
        headers_settings = settings_factory.get(SettingsType.HEADERS)
        middleware_settings = settings_factory.get(SettingsType.MIDDLEWARE)
        seeds_settings = settings_factory.get(SettingsType.SEEDS)
        source_settings = settings_factory.get(SettingsType.SOURCE)
        time_settings = settings_factory.get(SettingsType.TIME)
        has_gibbon = monkey_settings.has(MonkeyType.GIBBON)
        has_macaque = monkey_settings.has(MonkeyType.MACAQUE)

        request_dup_filter = filter_settings.get(FilterType.REQUEST_FILTER)
        source_dup_filter = filter_settings.get(FilterType.SOURCE_FILTER)
        max_idle_time = time_settings.get()
        crawling_delay = time_settings.get(TimeType.DELAY)
        seeds_key = seeds_settings.get()
        source_key = source_settings.get()
        queue_timeout, max_seeds_size, max_buffer_time = concurrency_settings.get()
        download_middlewares = middleware_settings.get(MonkeyType.MACAQUE)
        deploy_mode = deploy_settings.get()
        gibbons = monkey_settings.get(MonkeyType.GIBBON)
        orangutans = monkey_settings.get(MonkeyType.ORANGUTAN)

        [orangutan.when_wake_up() for orangutan in orangutans]
        logger.info("MACAQUE's domain: All Orangutans woke up, waiting for processing page source's items") \
            if len(orangutans) > 0 else None

        async def __gather(requests):
            __results = await asyncio.gather(*requests)
            return [Response(url=result[0], page_source=result[1], status_code=result[2]) for result in __results]

        def __prepare(requests):
            for request in requests:
                __headers = headers_settings.get()
                request.add_headers(__headers) if __headers else None

            for download_middleware in download_middlewares:
                for request in requests:
                    if hasattr(download_middleware, "prepare"):
                        download_middleware.prepare(request)

        def __do_request(requests):
            __responses = []
            for download_middleware in download_middlewares:
                if not hasattr(download_middleware, "on_request"):
                    continue

                for request in requests:
                    time.sleep(crawling_delay) if crawling_delay > 0 else None
                    if hasattr(download_middleware, "on_request"):
                        __response = download_middleware.on_request(request)
                        if not isinstance(__response, Response):
                            logger.warning("The download middleware must provide "
                                           "the on_request method and return a Response object")
                            break
                        __responses.append(__response)
                break

            if not __responses:
                __async_requests = []
                for request in requests:
                    time.sleep(crawling_delay) if crawling_delay > 0 else None
                    __async_requests.append(request.do_request())
                __responses = asyncio.run(__gather(__async_requests)) if len(__async_requests) > 0 else []
            return __responses

        def __on_request_finished(responses):
            for download_middleware in download_middlewares:
                for response in responses:
                    if hasattr(download_middleware, "on_finish"):
                        download_middleware.on_finish(response)

        def __transfer(values):
            __serve_forever = True
            for value in values:
                if isinstance(value, (Request,)):
                    if deploy_mode == OceanMonkey.LOCAL:
                        if value.refuse_filter or not request_dup_filter.seen(value, local=True):
                            macaque_queue.put(pickle.dumps(value))
                    elif deploy_mode == OceanMonkey.CLUSTER:
                        __seed_queue = Queues.next_queue(seed_queues)
                        if not request_dup_filter.server:
                            request_dup_filter.server = __seed_queue.server
                        if value.refuse_filter or not request_dup_filter.seen(value):
                            __seed_queue.put(pickle.dumps(value), keys=seeds_key)

                elif isinstance(value, (Signal, )):
                    macaque_queue.put(pickle.dumps(value))
                else:
                    [orangutan.process_item(value) for orangutan in orangutans]
            return __serve_forever

        def __schedule(requests):
            __responses = __do_request(requests)
            __on_request_finished(__responses)

            for index, response in enumerate(__responses):
                __responses[index].meta = requests[index].meta
                __responses[index].callback = requests[index].callback

            if deploy_mode == OceanMonkey.LOCAL:
                if has_gibbon:
                    for response in __responses:
                        if source_dup_filter.seen(response, local=True):
                            response.repeated = True
                        logger.info("Ocean Monkey work in local mode and there is gibbon, "
                                    "just transfer response to gibbon queue")
                        gibbon_queue = Queues.next_queue(gibbon_queues)
                        gibbon_queue.put(pickle.dumps(response.get_init_args())) if gibbon_queue \
                            else bye.bye("You must configure at least one gibbon",
                                         fn=__name__, lno=current_frame().f_lineno)

                elif has_macaque:
                    for __response in __responses:
                        if source_dup_filter.seen(__response, local=True):
                            __response.repeated = True

                        logger.info("Ocean Monkey work in local mode and there is only macaque,"
                                    "just play the role of gibbon")

                        if not __response.callback:
                            __response_coroutine = None
                            for gibbon in gibbons:
                                if hasattr(gibbon, "allowed_domains"):
                                    if domain(__response.url) in gibbon.allowed_domains:
                                        __response_coroutine = gibbon.parse(__response)
                                else:
                                    __response_coroutine = gibbon.parse(__response)
                                results = [result for result in __response_coroutine] if __response_coroutine else []
                                __transfer(results)
                        else:
                            __response_coroutine = __response.parse(__response)
                            __results = [result for result in __response_coroutine]
                            __transfer(__results)

            elif deploy_mode == OceanMonkey.CLUSTER:
                if has_gibbon:
                    for __response in __responses:
                        __source_queue = Queues.next_queue(source_queues)
                        if not source_dup_filter.server:
                            source_dup_filter.server = __source_queue.server

                        if source_dup_filter.seen(__response):
                            __response.repeated = True

                        logger.info("Ocean Monkey work in cluster mode and there is gibbon,"
                                    "just transfer response to gibbon queue")
                        __include_page_source = True if not __response.repeated else False
                        __gibbon_queue = Queues.next_queue(gibbon_queues)
                        __gibbon_queue.put(pickle.dumps(__response.get_init_args(
                            include_page_source=__include_page_source))) if __gibbon_queue else \
                            bye.bye("You must configure at least one gibbon", fn=__name__, lno=current_frame().f_lineno)
                else:
                    for __response in __responses:
                        __source_queue = Queues.next_queue(source_queues)
                        if not source_dup_filter.server:
                            source_dup_filter.server = __source_queue.server

                        if source_dup_filter.seen(__response):
                            __response.repeated = True

                        logger.info("Ocean Monkey work in cluster mode and there is only macaque,"
                                    "just transfer response to server's source queue")
                        __include_page_source = True if not __response.repeated else False
                        __source_queue.put(pickle.dumps(__response.get_init_args(
                            include_page_source=__include_page_source)), keys=source_key)

        def __consume():
            __serve_forever = True
            idle_time = 0
            while __serve_forever:
                seeds_waiter.acquire()
                try:
                    __value = macaque_queue.get(timeout=queue_timeout)
                    idle_time = 0
                except(Exception, ):
                    idle_time += queue_timeout
                    if max_idle_time is not None and idle_time >= max_idle_time:
                        say_goodbye_signal = pickle.dumps(Signal(SignalValue.TOO_IDLE))
                        seeds.append(say_goodbye_signal)
                        logger.info("Macaque was fired for being too idle")
                        seeds_waiter.notify()
                        seeds_waiter.release()
                        break
                    seeds_waiter.release()
                    continue

                seeds.append(__value)
                if len(seeds) >= max_seeds_size:
                    seeds_waiter.notify()
                seeds_waiter.release()

        def __batch_download():
            __serve_forever = True
            __excluding_domains_cache = {None, }
            while __serve_forever:
                seeds_waiter.acquire()
                if len(seeds) < max_seeds_size:
                    seeds_waiter.wait(timeout=max_buffer_time)
                __seeds_copy = copy.deepcopy(seeds) if seeds else []
                seeds.clear() if seeds else None
                seeds_waiter.release()

                __http_requests = []
                for __value in __seeds_copy:
                    try:
                        __value = pickle.loads(__value)
                        if isinstance(__value, (Request, )):
                            __http_requests.append(__value) if domain(__value.url) not in __excluding_domains_cache else None
                        elif isinstance(__value, (Signal, )):
                            if __value.value == SignalValue.SAY_GOODBYE:
                                __excluding_domains_cache.add(domain(__value.url))
                            elif __value.value == SignalValue.TOO_IDLE:
                                __serve_forever = False
                                break
                    except (KeyError,):
                        __url = __value.decode() if isinstance(__value, bytes) else None
                        __http_requests.append(Request(url=__url)) if domain(__url) not in __excluding_domains_cache else None

                __prepare(__http_requests)
                __schedule(__http_requests)

        _threads = [threading.Thread(target=__consume), threading.Thread(target=__batch_download)]
        [_thread.start() for _thread in _threads]
        [_thread.join() for _thread in _threads]
        [orangutan.when_sleep() for orangutan in orangutans]

    @staticmethod
    def _consume_sources(settings_path, gibbon_queue, macaque_queues):
        settings = importlib.import_module(settings_path)
        serve_forever = True
        seed_queues = SimpleQueueFactory.get_queues(settings, QueueType.SEEDS)

        settings_factory = SimpleSettingsFactory(settings)
        deploy_settings = settings_factory.get(SettingsType.DEPLOY)
        filter_settings = settings_factory.get(SettingsType.FILTERS)
        monkey_settings = settings_factory.get(SettingsType.MONKEY)
        seeds_settings = settings_factory.get(SettingsType.SEEDS)
        time_settings = settings_factory.get(SettingsType.TIME)

        max_idle_time = time_settings.get()
        deploy_mode = deploy_settings.get()
        request_dup_filter = filter_settings.get(FilterType.REQUEST_FILTER)

        gibbons = monkey_settings.get(MonkeyType.GIBBON)
        orangutans = monkey_settings.get(MonkeyType.ORANGUTAN)
        [orangutan.when_wake_up() for orangutan in orangutans]
        logger.info("GIBBON's domain: All Orangutans woke up, waiting for processing page source's items") \
            if len(orangutans) > 0 else None

        def __schedule(values):
            for value in values:
                if isinstance(value, (Request,)):
                    if deploy_mode == OceanMonkey.LOCAL:
                        if value.refuse_filter or not request_dup_filter.seen(value, local=True):
                            __macaque_queue = Queues.next_queue(macaque_queues)
                            logger.info("Transfer Request <{}> to Macaque queue".format(value.url))
                            __macaque_queue.put(pickle.dumps(value)) if __macaque_queue else None

                    elif deploy_mode == OceanMonkey.CLUSTER:
                        __seed_queue = Queues.next_queue(seed_queues)
                        if not request_dup_filter.server:
                            request_dup_filter.server = __seed_queue.server

                        if value.refuse_filter or not request_dup_filter.seen(value):
                            __seed_queue.put(pickle.dumps(value), keys=seeds_settings.get())

                elif isinstance(value, (Signal, )):
                    if value.value == SignalValue.SAY_GOODBYE:
                        logger.info("Gibbon receive a say-goodbye's signal on <{}>".format(value.url))
                        # __serve_forever = False
                        say_goodbye_signal = pickle.dumps(Signal(SignalValue.SAY_GOODBYE, value.url))
                        for macaque_queue in Queues.all_queues(macaque_queues):
                            macaque_queue.put(say_goodbye_signal)
                        # break
                else:
                    [orangutan.process_item(value) for orangutan in orangutans]

        while serve_forever:
            logger.info("Getting source from server's source queue or macaque...")
            try:
                _init_args = pickle.loads(gibbon_queue.get(timeout=max_idle_time))
            except (Exception, ):
                logger.info("Gibbon was fired for being too idle")
                serve_forever = False
                continue

            _response = Response(**_init_args)
            for gibbon in gibbons:
                if hasattr(gibbon, "allowed_domains"):
                    if domain(_response.url) not in gibbon.allowed_domains:
                        continue
                if not _response.callback:
                    results = gibbon.parse(_response)
                else:
                    results = _response.parse(_response)
                __schedule(results) if results else None

        [orangutan.when_sleep() for orangutan in orangutans]

    def _init_monkey_queues(self):
        if not hasattr(self.settings, "MONKEYS"):
            bye.bye("You must configure the monkeys in settings.py", fn=__name__, lno=current_frame().f_lineno)

        for monkey_type, monkeys in getattr(self.settings, "MONKEYS").items():
            if monkey_type not in self.__monkey_queues:
                self.__monkey_queues[monkey_type] = [1]
            for _ in range(monkeys):
                queue = multiprocessing.Queue()
                self.__monkey_queues[monkey_type].append(queue)

    def __get_monkey_queues(self, monkey_type):
        return self.__monkey_queues[monkey_type] if monkey_type in self.__monkey_queues else []

    def _launch_monkeys(self):
        macaque_queues = self.__get_monkey_queues(MonkeyType.MACAQUE)
        gibbon_queues = self.__get_monkey_queues(MonkeyType.GIBBON)

        def _launch_macaque_monkeys():
            for queue in macaque_queues[1:]:
                macaque = multiprocessing.Process(
                    target=self.__monkeys[MonkeyType.MACAQUE],
                    args=(self.__settings_path, queue, gibbon_queues))
                macaque.start()
                self.__macaque_monkeys.append(macaque)

        def _launch_gibbon_monkeys():
            for queue in gibbon_queues[1:]:
                gibbon = multiprocessing.Process(
                    target=self.__monkeys[MonkeyType.GIBBON],
                    args=(self.__settings_path, queue, macaque_queues))
                gibbon.start()
                self.__gibbon_monkeys.append(gibbon)

        _launch_macaque_monkeys()
        _launch_gibbon_monkeys()

    def _wait_for_monkeys(self):
        [monkey.join() for monkey in self.__macaque_monkeys]
        [monkey.join() for monkey in self.__gibbon_monkeys]

    def _init_seed_and_source_queues(self):
        self.__seed_queues = SimpleQueueFactory.get_queues(self.settings, QueueType.SEEDS)
        self.__source_queues = SimpleQueueFactory.get_queues(self.settings, QueueType.SOURCE)
        if not self.__seed_queues and not self.__source_queues:
            bye.bye("You must configure the seeds queue or source queue", fn=__name__, lno=current_frame().f_lineno)

    def _init_seed_workers(self):
        self.__seed_workers = []
        settings_factory = SimpleSettingsFactory(self.settings)
        monkey_settings = settings_factory.get(SettingsType.MONKEY)
        queue_settings = settings_factory.get(SettingsType.QUEUE)

        if monkey_settings.has(MonkeyType.MACAQUE) and queue_settings.has(QueueType.SEEDS):
            for seed_queue in self.__seed_queues[1:]:
                thread = threading.Thread(target=self._produce_seeds,
                                          args=(self.__settings_path, seed_queue,
                                                self.__monkey_queues[MonkeyType.MACAQUE],
                                                self.__macaque_monkeys, self.__seeds_lock))
                self.__seed_workers.append(thread)

    def _init_source_workers(self):
        self.__source_workers = []
        settings_factory = SimpleSettingsFactory(self.settings)
        monkey_settings = settings_factory.get(SettingsType.MONKEY)
        queue_settings = settings_factory.get(SettingsType.QUEUE)

        if monkey_settings.has(MonkeyType.GIBBON) and queue_settings.has(QueueType.SOURCE):
            for source_queue in self.__source_queues[1:]:
                thread = threading.Thread(target=self._produce_source,
                                          args=(self.__settings_path, source_queue,
                                                self.__monkey_queues[MonkeyType.GIBBON],
                                                self.__gibbon_monkeys, self.__source_lock))
                self.__source_workers.append(thread)

    def _launch_workers_and_wait(self):
        all_workers = self.__seed_workers + self.__source_workers
        [worker.start() for worker in all_workers]
        [worker.join() for worker in all_workers]

    def serve_forever(self):
        self._init_seed_and_source_queues()
        self._init_monkey_queues()
        self._launch_monkeys()
        self._init_seed_workers()
        self._init_source_workers()
        self._launch_workers_and_wait()
