import importlib
import inspect

from oceanmonkey.core.monkey import Macaque,Gibbon,Orangutan
from oceanmonkey.core.monkey import MonkeyType


class Monkey:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, settings):
        self.__settings = settings

    def has(self, monkey_type=MonkeyType.MACAQUE):
        settings = self.__settings
        monkeys = settings.MONKEYS[monkey_type] if monkey_type in settings.MONKEYS else 0
        return monkeys if monkeys > 0 else 0


    def get(self, monkey_type=MonkeyType.MACAQUE):
        settings = self.__settings
        gibbons_modules = settings.GIBBONS_MODULES if hasattr(settings,
                                                                "GIBBONS_MODULES") else [None]
        orangutans_modules = settings.ORANGUTANS_MODULES if hasattr(settings,
                                                                      "ORANGUTANS_MODULES") else [None]

        monkeys_modules = {
            MonkeyType.GIBBON: gibbons_modules[0],
            MonkeyType.ORANGUTAN: orangutans_modules[0]
        }

        monkeys_module = importlib.import_module(monkeys_modules[monkey_type])

        monkey_base_classes = {
            MonkeyType.GIBBON: Gibbon,
            MonkeyType.MACAQUE: Macaque,
            MonkeyType.ORANGUTAN: Orangutan
        }

        monkeys = []
        for name, cls in inspect.getmembers(monkeys_module, inspect.isclass):
            if cls.__base__ == monkey_base_classes[monkey_type]:
                if monkey_type == MonkeyType.GIBBON:
                    monkeys.append(cls())
                elif monkey_type == MonkeyType.ORANGUTAN:
                    monkeys.append(cls.have_a_monkey(settings.__dict__))
        return monkeys
