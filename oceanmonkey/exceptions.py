"""
OceanMonkey core exceptions
"""


class NotConfigured(Exception):
    """Indicates a missing configuration situation"""
    pass


class _InvalidOutput(TypeError):
    """
    Indicates an invalid value has been returned by a middleware's processing method.
    Internal and undocumented, it should not be raised or caught by user code.
    """
    pass



class IgnoreRequest(Exception):
    """Indicates a decision was made not to process a request"""


class DontCloseSpider(Exception):
    """Request the spider not to be closed yet"""
    pass


class CloseSpider(Exception):
    """Raise this from callbacks to request the spider to be closed"""

    def __init__(self, reason='cancelled'):
        super().__init__()
        self.reason = reason


class StopDownload(Exception):
    """
    Stop the download of the body for a given response.
    The 'fail' boolean parameter indicates whether or not the resulting partial response
    should be handled by the request errback. Note that 'fail' is a keyword-only argument.
    """

    def __init__(self, *, fail=True):
        super().__init__()
        self.fail = fail



class NotSupported(Exception):
    """Indicates a feature or method is not supported"""
    pass


# Commands
class UsageError(Exception):
    """To indicate a command-line usage error"""

    def __init__(self, *a, **kw):
        self.print_help = kw.pop('print_help', True)
        super().__init__(*a)