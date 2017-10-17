# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
import models
import forms

# Register your models here.

@admin.register(models.Consultorio)
class Consultorio(admin.ModelAdmin):
    list_display = ['nombre', 'celular', 'direccion', 'nit', 'correo', 'hora_maxima']
    search_fields = list_display
    icon = '<i class="material-icons">local_hospital</i>'

    def has_add_permission(self, request):
        consultorio = models.Consultorio.objects.first()
        if consultorio:
            return False
        return True
    # end def
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

class DuracionCitaStack(admin.TabularInline):
    model = models.DuracionCita
    readonly_fields = ('duracion_r',)
    extra = 0
# end class

class CitaReprogramadaStack(admin.StackedInline):
    model = models.CitaReprogramada
    form = forms.ReprogramarCitaForm
    extra = 3
    max_num = 3

    def get_readonly_fields(self, request, obj=None, **kwargs):
        if obj:
            if obj.confirmacion == 2:
                return self.readonly_fields + ('calendario', 'motivo', )
            # end if
        # end if
        return self.readonly_fields
    # end def
# end class


@admin.register(models.CitaMedica)
class CitaMedica(admin.ModelAdmin):
    list_display = ['paciente', 'procedimiento', 'entidad', 'confirmacion', 'motivo', 'fecha_canelacion', 'estado']
    list_filter = ['procedimiento', 'entidad', 'estado', 'confirmacion', 'calendario__inicio']
    search_fields = ['paciente__first_name', 'paciente__last_name', 'paciente__identificacion']
    icon = '<i class="material-icons">insert_invitation</i>'
    inlines = [CitaReprogramadaStack]
    form = forms.CitaMedicaForm

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            if obj.confirmacion == 2:
                return self.readonly_fields + ('paciente', 'procedimiento', 'entidad', 'calendario', 'confirmacion', 'motivo')
            # end if
            return self.readonly_fields + ('paciente', 'procedimiento', 'calendario', 'entidad')
        # end if
        return self.readonly_fields
    # end if

    class Media:
        js = ("agenda/js/cita.js", )
        css = {
            "all": ('agenda/css/fullcalendar.min.css', 'agenda/css/style.css')
        }
    # end class
# end class
