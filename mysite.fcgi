#!/home2/dranilsa/.virtualenvs/citas/bin/python
# -*- coding: utf-8 -*-
import sys, os

# Add a custom Python path.
sys.path.insert(0, "/home2/dranilsa/.virtualenvs/citas")
sys.path.insert(13, "/home2/dranilsa/public_html/app/Citas")
os.environ['DJANGO_SETTINGS_MODULE'] = 'Citas.settings'
from django_fastcgi.servers.fastcgi import runfastcgi
from django.core.servers.basehttp import get_internal_wsgi_application
wsgi_application = get_internal_wsgi_application()
runfastcgi(wsgi_application, method="prefork", daemonize="false", minspare=1, maxspare=1, maxchildren=1)
