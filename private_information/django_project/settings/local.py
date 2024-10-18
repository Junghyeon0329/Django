from django_project.settings.base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "homepage_private",
        "USER": "root",
        "PASSWORD": "test",
        "HOST": "127.0.0.1",
        "PORT": "3306",
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
