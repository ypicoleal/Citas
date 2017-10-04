# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from supra import views as supra
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from Citas.decorator import check_login
from django.views.decorators.csrf import csrf_exempt
from usuarios.models import Paciente
import models
import forms
supra.SupraConf.body = True
# Create your views here.

"""
    CalendarioCita
"""
class CalendarioCitaList(supra.SupraListView):
    model = models.CalendarioCita
    list_display = ['id', 'title', 'start', 'end', 'color', 'almuerzo', 'asignacionCita', 'name']
    list_filter = ['inicio__year', 'inicio__month', 'inicio__day', 'almuerzo']

    def start(self, obj, row):
        return obj.inicio.strftime('%Y-%m-%d %H:%M:%S')

    def end(self, obj, row):
        return obj.fin.strftime('%Y-%m-%d %H:%M:%S')

    def name(self, obj, row):
        return u"%s %s" % (obj.inicio.strftime('%H:%M:%S'), obj.fin.strftime('%H:%M:%S'))

    def asignacionCita(self, obj, row):
        asignacion = models.CitaMedica.objects.filter(calendario=obj).first()
        if asignacion:
            nombre = "%s %s" % (asignacion.paciente.first_name, asignacion.paciente.last_name)
            return {"id": asignacion.id, "nombre": nombre}
        return None

    def title(self, obj, row):
        title = "Espacio para cita"
        if obj.almuerzo:
            title = "Almuerzo"
        asignacion = self.asignacionCita(obj, row)
        if asignacion:
            title = "Cita: %s" % asignacion["nombre"]
        return title

    def color(self, obj, row):
        color = "#2196f3"
        if obj.almuerzo:
            color = "#f44336"
        elif self.asignacionCita(obj, row):
            color = "#9c27b0"
        return color

    @method_decorator(check_login)
    def dispatch(self, request, *args, **kwargs):
        return super(CalendarioCitaList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        filtro = self.request.GET.get('citamedica', False)
        queryset = super(CalendarioCitaList, self).get_queryset()
        if filtro:
            queryset = queryset.filter(citamedica=None)
        return queryset.filter(eliminado=False)
    # end def
# end class


class CalandarioCitaForm(supra.SupraFormView):
    model = models.CalendarioCita
    form_class = forms.CalendarioCitaForm

    def get_form_class(self):
        if 'pk' in self.http_kwargs:
            self.form_class = forms.CalendarioCitaFormEdit
        # end if
        return self.form_class
    # end class

    @method_decorator(check_login)
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(CalandarioCitaForm, self).dispatch(request, *args, **kwargs)


class CalandarioCitaDelete(supra.SupraDeleteView):
    model = models.CalendarioCita

    @method_decorator(check_login)
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(CalandarioCitaDelete, self).dispatch(request, *args, **kwargs)
    # end def

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        asignacion = models.CitaMedica.objects.filter(calendario=self.object).first()
        if not asignacion:
            self.object.eliminado = True
            self.object.save()
            return HttpResponse({"exito": "eliminado"},status=200, content_type="application/json")
        else:
            return HttpResponse({"error": "No se puede borrar porque existe una cita agenda para esta fecha"}, status=400, contentType="application/json")
    # end def
# end class

"""
    CitaMedica
"""


class CitasMedicasList(supra.SupraListView):
    model = models.CitaMedica
    list_display = ['paciente', 'procedimiento', 'entidad', 'estado', 'confirmacion']
    list_filter = ['paciente', 'procedimiento', 'entidad', 'estado', 'confirmacion', 'calendario__inicio__year', 'calendario__inicio__month', 'calendario__inicio__day']

    @method_decorator(check_login)
    def dispatch(self, request, *args, **kwargs):
        return super(CitasMedicasList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(CitasMedicasList, self).get_queryset()
        paciente = Paciente.objects.filter(id=self.request.user.pk).first()
        if paciente:
            queryset = queryset.filter(paciente=paciente.id)
        return queryset
    # end def
# end class

class CitaMedicaForm(supra.SupraFormView):
    model = models.CitaMedica
    form_class = forms.CitaMedicaFormSupra

    @method_decorator(check_login)
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(CitaMedicaForm, self).dispatch(request, *args, **kwargs)

# end class

"""
    Procedimientos
"""

class ProcedimientosList(supra.SupraListView):
    model = models.ProcedimientoMedico
    list_display = ['nombre', 'precio', 'modalidad']
    search_fields = ['nombre', 'precio']
    list_filter = ['modalidad', ]

    @method_decorator(check_login)
    def dispatch(self, request, *args, **kwargs):
        return super(ProcedimientosList, self).dispatch(request, *args, **kwargs)
# end class
