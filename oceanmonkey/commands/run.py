import os
import importlib
import sys
from configparser import ConfigParser
from oceanmonkey.commands import MonkeyCommand
from oceanmonkey.core.engine import OceanMonkey
import oceanmonkey.utils as utils


class Run(MonkeyCommand):
    __supported_opts = {"-h", }

    def __init__(self, args):
        super().__init__()
        self.__opts = self.__parse_args(args)
        self.__opts_callback = {
            "-h": self.print_help
        }

    def __parse_args(self, args):
        opts = []
        for index, arg in enumerate(args):
            if arg.startswith("-"):
                opts.append(arg)
        return opts

    def print_help(self):
        print("Usage:")
        print("monkeys run -h")
        print("desc:run the OceanMonkey app for crawling data")
        print("e.g.: monkeys run")

    @staticmethod
    def __serve_forever(cfg_file="oceanmonkey.cfg"):
        if  cfg_file in os.listdir():
            config = ConfigParser()
            config.read(cfg_file)
            app_settings_module_path = config.get("settings", "default")
            if not app_settings_module_path:
                print("Error: You need to specify the project's settings file in {}".format(cfg_file))
            else:
                sys.path.append(os.getcwd())
                ocean_monkey = OceanMonkey(app_settings_module_path)
                ocean_monkey.serve_forever()
        else:
            print("Error: you are not in the OceanMonkey project's top-level directory")

    def execute(self):
        if not self.__opts:
            self.__serve_forever()
        else :
            [self.__opts_callback[opt]() for opt in self.__opts]
