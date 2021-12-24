from traceback import format_exc
from sys import argv, exit

from cli import *
from helpers import *
from commands import *

if __name__ == "__main__":

    # empty args
    if len(argv) == 1:
        # help
        help()
        exit(1)

    # command decomposition
    command, args = argv[1], argv[2:]

    if command in commands:
        try:
            if command == commands[0]:
                # help
                help()
            elif command == commands[1]:
                # new
                output("o", "New")
                new(args)

            # healthy finish
            output("o", "Completed")
            exit(0)
        except Exception as e:
            output("o", "Aborted")
            output("e", e)
            print(format_exc())
            exit(1)
    else:
        output("e", "Unrecognised command: " + command)
        help()
        exit(1)
