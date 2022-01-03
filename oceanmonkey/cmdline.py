import sys
from oceanmonkey.utils import commands


def _pop_command_name(argv):
    i = 0
    subcommand = None
    opts = []
    for arg in argv[1:]:
        if not arg.startswith('-'):
            if not subcommand:
                subcommand = arg
                del argv[i]
                break
        else:
            opts.append(arg)
        i += 1
    return subcommand, opts


def _print_help():
    print("Usage:")
    print("monkeys [startproject | be | run] [-h]")
    print("detailed info about monkeys' subcommand, please enter monkeys subcommand -h")
    print("e.g.: monkeys startproject -h")


def execute(argv=None):
    argv = argv or sys.argv
    command, opts = _pop_command_name(argv)
    commands.execute_command(command, argv[1:]) if command else _print_help()


if __name__ == '__main__':
    execute()
