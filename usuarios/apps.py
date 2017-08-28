# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class UsuariosConfig(AppConfig):
    name = 'usuarios'
    icon = '<i class="material-icons">account_circle</i>'
    
    def ready(self):
        import signals
