import os
from oceanmonkey.commands import MonkeyCommand
from oceanmonkey.core.template import ProjectTemplate


class StartProjectCommand(MonkeyCommand):
    __supported_opts = {"-h", }

    def __init__(self, args):
        super().__init__()
        self.__project_name, self.__opts = self.__parse_args(args)
        self.__opts_callback = {
            "-h": self.print_help
        }

    def __parse_args(self, args):
        project_name = None
        opts = []
        for index, arg in enumerate(args):
            if arg.startswith("-"):
                opts.append(arg) if arg in self.__supported_opts else None
            else:
                if index != 0:
                    opts.clear()
                    break
                project_name = arg
        return project_name, opts

    def print_help(self):
        print("Usage:")
        print("monkeys startproject <project_name | -h>\n")
        print("e.g.:monkeys startproject OceanMonkey")
        print(r"e.g.:monkeys startproject D:\OceanMonkey")
        print("e.g.:monkeys startproject /usr/local/OceanMonkey")
        print("e.g.:monkeys startproject -h")

    def __create_project(self):
        if self.__project_name in os.listdir():
            print("Error:directory exists, please enter a new directory!")
        else:
            ProjectTemplate(self.__project_name).create()
            print("OceanMonkey project {} created.".format(os.path.basename(self.__project_name)))


    def execute(self):
        if not self.__project_name and not self.__opts:
            print("Invalid command operation.")
            self.print_help()
        elif self.__project_name and self.__opts:
            print("Invalid command operation.")
            self.print_help()
        elif self.__project_name:
            self.__create_project()
        elif self.__opts:
            [self.__opts_callback[opt]() for opt in self.__opts]
