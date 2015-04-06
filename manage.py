#!/usr/bin/env python2
import os
import sys

if __name__ == '__main__':
    sys.path.insert(0, os.path.join(os.getcwd(), 'wizfs'))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wizfs.settings')
    os.environ.setdefault('DJANGO_CONFIGURATION', 'Local')
    from configurations.management import execute_from_command_line

    execute_from_command_line(sys.argv)
