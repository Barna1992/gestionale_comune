"""
WSGI config for gestione_comune project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestione_comune.settings.production')

application = get_wsgi_application()
