from .base import *


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

SECRET_KEY = 'sntaoheuswvmaosenuh8aoe9782(*santoeussatnoe'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS += [ 'hussle.net.isc.upenn.edu' ]

STATIC_ROOT = '/home/charlesr/code/PennDevice/PennDevice/static/'
STATIC_URL = '/static/'

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
