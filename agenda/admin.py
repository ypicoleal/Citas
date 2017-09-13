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
# end class

@admin.register(models.ProcedimientoMedico)
class ProcedimientoMedico(admin.ModelAdmin):
    list_display = ['nombre', 'precio', 'modalidad']
    search_fields = ['nombre', ]
    icon = '<i class="material-icons">local_pharmacy</i>'
# end class

@admin.register(models.CalendarioCita)
class CalendarioCita(admin.ModelAdmin):
    list_display = ['inicio', 'fin', 'almuerzo']
    list_display_links = None
    icon = '<i class="material-icons">date_range</i>'

    class Media:
        css = {
            "all": ('agenda/css/fullcalendar.min.css', 'agenda/css/style.css')
        }
        js = ('agenda/js/librerias/moment.min.js', 'agenda/js/fullcalendar.min.js', 'agenda/js/locale-all.js', 'agenda/js/calendario.js', )

    def has_add_permission(self, request):
        return False
    # end def

    def has_delete_permission(self, request, obj=None):
        return False
    # end def

    def get_queryset(self, request):
        queryset = super(CalendarioCita, self).get_queryset(request)
        return queryset.exclude(admin=False)
    # end def
# end class

@admin.register(models.CitaMedica)
class CitaMedica(admin.ModelAdmin):
    list_display = ['paciente', 'procedimiento', 'entidad', 'reprogramar', 'estado', 'confirmacion']
    list_filter = ['paciente', 'procedimiento', 'entidad', 'estado', 'confirmacion']
    icon = '<i class="material-icons">insert_invitation</i>'
# end class
