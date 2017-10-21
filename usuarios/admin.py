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
        actions = super(MedicoAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        # end if
        return actions
    # end def
# end class

@admin.register(usuarios.Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('identificacion', 'first_name', 'last_name', '_tipo', 'email', 'fecha_nacimiento', 'estado_civil', 'profesion', 'telefono', 'eliminado')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'identificacion', 'cedula_a', 'telefono')
    icon = '<i class="material-icons">person_outline</i>'
    form = forms.PacienteAdmin
    actions = ['eliminar_paciente']

    class Media:
        js = ("usuarios/paciente.js", )
    # end class

    def has_delete_permission(self, request, obj=None):
        return False
    # end def

    def eliminar_paciente(self, request, queryset):
        rows_updated = queryset.update(eliminado=True)
        if rows_updated == 1:
            message_bit = "1 paciente fue correctamente eliminado"
        else:
            message_bit = "%s pacientes fueron correctamente elimindos" % rows_updated
        self.message_user(request, "%s" % message_bit)
    # end def

    eliminar_paciente.short_description = "Eliminar pacientes seleccionados"

    def get_actions(self, request):
        actions = super(PacienteAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        # end if
        return actions
    # end def
# end class
