from .base import *


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

ALLOWED_HOSTS += [ 'hussle.net.isc.upenn.edu' ]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
