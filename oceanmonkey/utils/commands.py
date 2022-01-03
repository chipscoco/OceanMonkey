import importlib
import inspect
from oceanmonkey.commands import MonkeyCommand
from oceanmonkey.commands import CommandType

def has(command_name):
    return CommandType[command_name] if command_name in CommandType else 0

def execute_command(command, args, command_module_path="oceanmonkey.commands"):
    command_name = command.lower() if command else None
    if command_name:
        module_name = command_module_path+"."+command_name
        command_module = importlib.import_module(module_name)
        for name, cls in inspect.getmembers(command_module, inspect.isclass):
            if cls.__base__ == MonkeyCommand:
                cls(args).execute()
                break



