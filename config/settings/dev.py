from .base import *


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DEBUG=True

INSTALLED_APPS += [ 'rest_framework' ]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAdminUser',
    ],
    'PAGE_SIZE': 10
}


DEV = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
