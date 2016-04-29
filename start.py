#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "oss.settings")

    from django.core.management import execute_from_command_line
    while True:
        cmd = input('Input command or enter to run server or quit: ')
        if cmd == '':
            execute_from_command_line([sys.argv[0], 'runserver'])
        elif cmd == 'quit':
            quit()
        else:
            execute_from_command_line([sys.argv[0], cmd])
            quit()
