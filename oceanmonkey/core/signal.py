class SignalValue:
    TOO_IDLE = 0
    SAY_GOODBYE = 1

class Signal:
    def __init__(self, value = SignalValue.SAY_GOODBYE, url=None):
        self.__value = value
        self.__url = url

    @property
    def value(self):
        return self.__value

    @property
    def url(self):
        return self.__url
