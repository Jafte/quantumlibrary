#!/usr/bin/env python
import os
import sys

sys.path.append('/home/j/jaftefty/quantumlibrary.ru/quantumlibrary')
sys.path.append('/home/j/jaftefty/quantumlibrary.ru/venv/lib/python3.4/site-packages')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()