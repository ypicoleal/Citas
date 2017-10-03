#!/home2/dranilsa/.virtualenvs/citas/bin/python
import sys, os

# Add a custom Python path.
sys.path.insert(0, "/home2/dranilsa/.virtualenvs/citas")
sys.path.insert(13, "/home2/dranilsa/public_html/app/Citas")
os.environ['DJANGO_SETTINGS_MODULE'] = 'Citas.settings'  
from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")
