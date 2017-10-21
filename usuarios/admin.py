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
    list_display = ('identificacion', 'first_name', 'last_name', '_tipo', 'email', 'fecha_nacimiento', 'estado_civil', 'profesion', 'telefono')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'identificacion', 'cedula_a', 'telefono')
    icon = '<i class="material-icons">person_outline</i>'
    form = forms.PacienteAdmin
    actions = ['eliminar_paciente', 'recuperar_paciente']

    class Media:
        js = ("usuarios/paciente.js", )
    # end class

    def has_delete_permission(self, request, obj=None):
        return False
    # end def

    def get_list_display(self, request):
        if self.request.user.is_superuser:
            return self.list_display + ('eliminado',)
        # end if
        return self.list_display
    # end def

    def get_queryset(self, request):
        queryset = super(PacienteAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            return queryset.exclude(eliminado=True)

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

    def recuperar_paciente(self, request, queryset):
        rows_updated = queryset.update(eliminado=False)
        if rows_updated == 1:
            message_bit = "1 paciente fue correctamente recuperado"
        else:
            message_bit = "%s pacientes fueron correctamente recuperados" % rows_updated
        self.message_user(request, "%s" % message_bit)
    # end def


    recuperar_paciente.short_description = "Recuperar pacientes seleccionados"

    def get_actions(self, request):
        actions = super(PacienteAdmin, self).get_actions(request)
        if not request.user.is_superuser:
            if 'recuperar_paciente' in actions:
                del actions['recuperar_paciente']
            # end if
        # end if
        if 'delete_selected' in actions:
            del actions['delete_selected']
        # end if
        return actions
    # end def
# end class
