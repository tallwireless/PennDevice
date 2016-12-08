from .base import *


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

ALLOWED_HOSTS += [ 'hussle.net.isc.upenn.edu' ]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'penndevice-dev',
        'USER': 'penndevice-dev',
        'PASSWORD': '3c#BmdDCXyp4r!F2',
        'HOST': '127.0.0.1',
        'PORT': '5432', 
    }
}
