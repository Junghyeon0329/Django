#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# mkdir operational_system
# homepage\operational_system> django-admin startproject django_project operational_system
# homepage\operational_system> python manage.py startapp roles

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings.local')
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
    main()
