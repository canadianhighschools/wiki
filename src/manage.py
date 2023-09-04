#!/usr/bin/env python
import os
import sys
import logging

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
    

if __name__ == '__main__':
    logging.basicConfig(filename="latest.log", level=logging.INFO)

    main()