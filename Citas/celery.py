# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.decorators import task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Citas.settings')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Celery('citas')

# Using  a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@task(name="notificacion")
def notificacion(task):
    print "##### task id", task
    subject, from_email, to = "Comentarios", 'mariobarrpach@gmail.com', ["mariobarrpach@gmail.com"]
    text_content = "Test"
    html_content = "<p>Correo del emisor: mariobarrpach@gmail.com</p>"
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    # end def
