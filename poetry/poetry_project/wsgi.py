"""
WSGI config for poetry_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poetry_project.settings')

application = get_wsgi_application()

#sys.path.append(os.path.dirname(os.path.abspath(__file__)) + './dante/python/')
#sys.path.append('./dante/python/')

#path = os.path.abspath(os.path.join(__file__, '..', '..'))

#if path not in sys.path:
#    sys.path.append(path)