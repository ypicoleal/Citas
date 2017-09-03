# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
import models

# Register your models here.

@admin.register(models.Consultorio)
class Consultorio(admin.ModelAdmin):
    list_display = ['nombre', 'celular', 'direccion', 'nit', 'correo']
    search_fields = list_display
    icon = '<i class="material-icons">local_hospital</i>'
# end def
