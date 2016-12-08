"""
WSGI config for PennDevice project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os
from socket import gethostname

from django.core.wsgi import get_wsgi_application

if 'hussle' in gethostname():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.test")
elif 'penndevice' in gethostname():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.prod")
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.prod")

application = get_wsgi_application()
