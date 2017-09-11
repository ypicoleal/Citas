# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from usuarios import models as usuarios
import forms
admin.site.site_url = None
# Register your models here.

@admin.register(usuarios.Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ('identificacion', 'first_name', 'last_name', '_Tipo', 'email', 'fecha_nacimiento', 'numero_registro', 'nombre_u', 'telefono', 'especialidad')
    search_fields = ('username', 'email', 'first_name',
                     'last_name', 'identificacion')
    icon = '<i class="material-icons">person_outline</i>'
    form = forms.MedicoForm
# end class

@admin.register(usuarios.Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('identificacion', 'first_name', 'last_name', '_Tipo', 'email', 'fecha_nacimiento', 'estado_civil', 'profesion', 'telefono',)
    search_fields = ('username', 'email', 'first_name', 'last_name', 'identificacion', 'cedula_a', 'telefono')
    icon = '<i class="material-icons">person_outline</i>'
    form = forms.PacienteAdmin

    class Media:
        js = ("usuarios/paciente.js", )
# end class
