#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'workforcehub.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    # https://docs.djangoproject.com/ko/5.1/intro/tutorial01/   
    # sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))       
    # from URLaddress import workforceURL
    # sys.argv = ['manage.py', 'runserver', f"{workforceURL['ip']}:{workforceURL['port']}"]
    main()

