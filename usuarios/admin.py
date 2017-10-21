# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from usuarios import models as usuarios
import forms
admin.site.site_url = None
# Register your models here.

@admin.register(usuarios.Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ('identificacion', 'first_name', 'last_name', '_tipo', 'email', 'fecha_nacimiento', 'numero_registro', 'nombre_u', 'telefono', )
    search_fields = ('username', 'email', 'first_name',
                     'last_name', 'identificacion')
    icon = '<i class="material-icons">person_outline</i>'
    form = forms.MedicoForm

    def has_add_permission(self, request):
        medico = usuarios.Medico.objects.first()
        if medico:
            return False
        return True
    # end def

    def has_delete_permission(self, request, obj=None):
        return False
    # end def

    def get_actions(self, request):
        actions = super(CompraAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        # end if
        return actions
    # end def
# end class

@admin.register(usuarios.Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('identificacion', 'first_name', 'last_name', '_tipo', 'email', 'fecha_nacimiento', 'estado_civil', 'profesion', 'telefono',)
    search_fields = ('username', 'email', 'first_name', 'last_name', 'identificacion', 'cedula_a', 'telefono')
    icon = '<i class="material-icons">person_outline</i>'
    form = forms.PacienteAdmin

    class Media:
        js = ("usuarios/paciente.js", )
# end class
