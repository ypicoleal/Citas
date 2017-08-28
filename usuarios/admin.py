# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from usuarios import models as usuarios
import forms
# Register your models here.

@admin.register(usuarios.Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', '_tipo', 'identificacion', 'email', 'fecha_nacimiento', 'numero_registro', 'nombre_u', 'telefono', 'especialidad')
    search_fields = ('username', 'email', 'first_name',
                     'last_name', 'identificacion')
    icon = '<i class="material-icons">person_outline</i>'
    form = forms.MedicoForm
# end class
