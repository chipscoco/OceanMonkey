"""
This is the core filter class.
"""
import six
import abc
import hashlib
from w3lib.url import canonicalize_url
from oceanmonkey.core import request
from oceanmonkey.core.database import RedisDataType


class BaseDuplicatesFilter(abc.ABC):
    @abc.abstractmethod
    def seen(self, value, **kwargs):
        """ nothing to do, just  in a daze """

    @abc.abstractmethod
    def _calc_fingerprint(self, value, **kwargs):
        """ nothing to do, just  in a daze """

    @staticmethod
    def _to_bytes(text, encoding=None, errors='strict'):
        """Return the binary representation of `text`. If `text`
        is already a bytes object, return it as-is."""
        if isinstance(text, bytes):
            return text
        if not isinstance(text, six.string_types):
            raise TypeError('to_bytes must receive a unicode, str or bytes '
                            'object, got %s' % type(text).__name__)
        if encoding is None:
            encoding = 'utf-8'
        if not text:
            text = ''
        return text.encode(encoding, errors)

    @staticmethod
    def _fingerprint_seen(fingerprint, fingerprints, server, keys, **kwargs):
        seen = True
        local = kwargs["local"] if "local" in kwargs else False
        if local:
            if fingerprint not in fingerprints:
                fingerprints.add(fingerprint)
                seen = False
        else:
            if not server.exists(name=keys, value=fingerprint):
                server.add(fingerprint, keys=keys, data_type=RedisDataType.SET)
                seen = False

        return seen


class RequestDupFilter(BaseDuplicatesFilter):
    __fingerprint_cache = {}

    def __init__(self, server=None, keys="ocean_seeds:duplicates"):
        self.__local_fingerprints = set()
        self.__server = server
        self.__keys = keys

    @property
    def server(self):
        return self.__server

    @server.setter
    def server(self, server_):
        self.__server = server_

    def seen(self, value, **kwargs):
        return self._request_seen(value, **kwargs)

    @staticmethod
    def __get_values(values):
        values = values.split(";")
        values.sort()
        return values

    def __hash_on_request(self, hash_algorithm, request, include_headers=None):
        hash_algorithm.update(self._to_bytes(canonicalize_url(request.url)))
        hash_algorithm.update(self._to_bytes(request.method))
        hash_algorithm.update(b'' if not request.body else self._to_bytes(request.body))

        if include_headers:
            for header in include_headers:
                hash_algorithm.update(self._to_bytes(header))
                for v in self.__get_values(include_headers[header]):
                    hash_algorithm.update(self._to_bytes(v))

        return hash_algorithm.hexdigest()

    def __hash_on_url(self, hash_algorithm, url, include_headers=None):
        hash_algorithm.update(self._to_bytes(canonicalize_url(url)))
        if include_headers:
            for header in include_headers:
                hash_algorithm.update(self._to_bytes(header))
                for v in self.__get_values(include_headers[header]):
                    hash_algorithm.update(self._to_bytes(v))

        return hash_algorithm.hexdigest()

    def _calc_fingerprint(self, request_or_url, **kwargs):
        headers = None if "headers" not in kwargs else kwargs["headers"]
        cache_key = canonicalize_url(request_or_url.url) \
            if isinstance(request_or_url, request.Request) else canonicalize_url(request_or_url)
        cache = self.__fingerprint_cache.setdefault(cache_key, {})

        fingerprint_key = None
        if headers:
            fingerprint_key = tuple(self._to_bytes(h.lower())
                                    for h in sorted(headers.keys()))

        if fingerprint_key not in cache:
            sha1 = hashlib.sha1()
            cache[fingerprint_key] = self.__hash_on_request(sha1, request_or_url, headers) \
                if isinstance(request_or_url, request.Request) else self.__hash_on_url(sha1, request_or_url, headers)
        return cache[fingerprint_key]

    def _request_seen(self, request_or_url, **kwargs):
        fingerprint = self._calc_fingerprint(request_or_url, **kwargs)
        return self._fingerprint_seen(fingerprint, self.__local_fingerprints, self.__server, self.__keys, **kwargs)


class PageSourceDupFilter(BaseDuplicatesFilter):
    __fingerprint_cache = {}

    def __init__(self, server=None, keys="ocean_source:duplicates"):
        self.__local_fingerprints = set()
        self.__server = server
        self.__keys = keys

    @property
    def server(self):
        return self.__server

    @server.setter
    def server(self, server_):
        self.__server = server_

    def seen(self, value, **kwargs):
        return self._page_source_seen(value, **kwargs)

    def _page_source_seen(self, response, **kwargs):
        fingerprint = self._calc_fingerprint(response, **kwargs)
        return self._fingerprint_seen(fingerprint, self.__local_fingerprints, self.__server, self.__keys, **kwargs)

    def _calc_fingerprint(self, response, **kwargs):
        cache = self.__fingerprint_cache.setdefault(canonicalize_url(response.url), {})
        params = {} if "params" not in kwargs else kwargs["params"]
        fingerprint_key = None
        if params:
            fingerprint_key = tuple(self._to_bytes(h.lower())
                                    for h in sorted(params.keys()))

        if fingerprint_key not in cache:
            sha1 = hashlib.sha1()
            sha1.update(self._to_bytes(response.page_source))
            for k, v in params.items():
                sha1.update(self._to_bytes(k))
                sha1.update(self._to_bytes(v))

            cache[fingerprint_key] =  sha1.hexdigest()

        return cache[fingerprint_key]
