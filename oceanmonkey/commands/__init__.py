"""
Base class for OceanMonkey commands
"""
import abc


class MonkeyCommand(abc.ABC):
    @abc.abstractmethod
    def execute(self):
        """ """

    @abc.abstractmethod
    def print_help(self):
        """"""

CommandType = {
    "startproject": 1,
    "run": 2
}

class Commands:
    STARTPROJECT = CommandType["startproject"]
    RUN = CommandType["run"]
