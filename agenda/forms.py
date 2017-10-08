# -*- coding: utf-8 -*-
from django import forms
from django.db.models import Q
import models
import datetime
import calendar
from cuser.middleware import CuserMiddleware

def getTimeDifference(TimeStart, TimeEnd):
    timeDiff = TimeEnd - TimeStart
    return timeDiff.total_seconds() / 60

"""
    Calendario
"""
class CalendarioCitaForm(forms.ModelForm):

    class Meta:
        model = models.CalendarioCita
        exclude = ()

    def clean(self):
        cleaned_data = super(CalendarioCitaForm, self).clean()
        inicio = cleaned_data.get('inicio', False)
        fin = cleaned_data.get('fin', False)
        hoy = datetime.date.today()
        if inicio and fin:
            calendario = models.CalendarioCita.objects.filter(Q(inicio=inicio, fin=fin, eliminado=False)| Q(inicio__lt=fin, fin__gt=inicio, eliminado=False)).first()
            if calendario:
                raise forms.ValidationError("Ya existe una cita en ese este rango de fechas")
        if inicio:
            if inicio.date() <= hoy:
                raise forms.ValidationError("No se pueden crear calendarios de citas para días anteriores o iguales a la fecha actual")

    def clean_fin(self):
        fin = self.cleaned_data['fin']
        inicio = self.cleaned_data.get('inicio', False)
        if not fin:
            raise forms.ValidationError("Este campo es requerido")

        if inicio:
            print inicio, fin
            if inicio >= fin:
                raise forms.ValidationError("Fin debe ser mayor a inicio")
            elif getTimeDifference(inicio, fin) > 30:
                raise forms.ValidationError("El rango de fecha no puede superar los 30 minutos")

        return fin


class CalendarioCitaFormEdit(forms.ModelForm):

    class Meta:
        model = models.CalendarioCita
        exclude = ('inicio', 'fin')


"""
    Cita Medica
"""


class CitaMedicaForm(forms.ModelForm):
    fecha_ = forms.DateField(label="Filtro de fecha")

    def __init__(self, *args, **kwargs):
        super(CitaMedicaForm, self).__init__(*args, **kwargs)
        procedimiento = self.fields['procedimiento']
        procedimiento.queryset = models.ProcedimientoMedico.objects.filter(modalidad=1)
        procedimiento.widget.can_add_related = False
        procedimiento.widget.can_change_related = False

        calendario = self.fields['calendario']
        calendario.widget.can_add_related = False
        calendario.widget.can_change_related = False


        if hasattr(self, 'instance') and self.instance.pk:
            calendario.queryset = models.CalendarioCita.objects.filter(inicio__year=self.instance.calendario.inicio.year, inicio__month=self.instance.calendario.inicio.month)
            self.fields['fecha_'].initial = self.instance.calendario.inicio.strftime('%d/%m/%Y')
            calendario.widget.attrs['disabled'] = False

        else:
            hoy = datetime.date.today()
            calendario.queryset = models.CalendarioCita.objects.filter(inicio__year=hoy.year, inicio__month=hoy.month)
            calendario.widget.attrs['disabled'] = True

    class Meta:
        model = models.CitaMedica
        fields = ['paciente', 'procedimiento', 'entidad', 'fecha_', 'calendario', 'confirmacion']

    def clean_entidad(self):
        entidad = self.cleaned_data['entidad']
        calendario = self.cleaned_data.get('calendario', False)
        if not entidad:
            raise forms.ValidationError("Este campo es requerido")

        if calendario:
            if calendario.inicio.weekday() is 4 and calendario.inicio.hour >= 13 and not entidad is 1:
                raise forms.ValidationError("Lo sentimos. Solo hay disponibilidad de citas para particulares")
            elif calendario.inicio.weekday() is 5 and not entidad is 1:
                raise forms.ValidationError("Lo sentimos. Solo hay disponibilidad de citas para particulares")

        return entidad

    def clean_calendario(self):
        calendario = self.cleaned_data.get('calendario', False)
        if calendario:
            consultorio = models.Consultorio.objects.first()
            if datetime.datetime.today().day + 1 is calendario.inicio.day:
                if consultorio:
                    if consultorio.hora_maxima.hour >= datetime.datetime.today().hour:
                        raise forms.ValidationError("Por favor reserve para un dia posterior")
                elif 17 >= datetime.datetime.today().hour:
                    raise forms.ValidationError("Por favor reserve para un dia posterior")

            if calendario.inicio.date() <= datetime.date.today():
                raise forms.ValidationError("No se pueden asignar citas para días anteriores a la fecha actual")

            return calendario
        else:
            if hasattr(self, 'instance') and self.instance.pk:
                if self.instance.cancelar:
                    return calendario
            raise forms.ValidationError("Este campo es requerido")
    # end def
# end class


class CitaMedicaFormSupra(forms.ModelForm):

    class Meta:
        model = models.CitaMedica
        fields = ['procedimiento', 'entidad', 'calendario',]


    def clean(self):
        cleaned_data = super(CalendarioCitaForm, self).clean()
        if hasattr(self, 'instance') and self.instance.pk:
            return cleaned_data
        else:
            user = CuserMiddleware.get_user()
            paciente = models.Paciente.objects.filter(id=user.id).first()
            if not paciente:
                form.ValidationError("Necesita ser un paciente para crear una cita")
        # end if
    # end def

    def clean_entidad(self):
        entidad = self.cleaned_data['entidad']
        calendario = self.cleaned_data.get('calendario', False)
        if not entidad:
            raise forms.ValidationError("Este campo es requerido")

        if calendario:
            if calendario.inicio.weekday() is 4 and calendario.inicio.hour >= 13 and not entidad is 1:
                raise forms.ValidationError("Lo sentimos. Solo hay disponibilidad de citas para particulares")
            elif calendario.inicio.weekday() is 5 and not entidad is 1:
                raise forms.ValidationError("Lo sentimos. Solo hay disponibilidad de citas para particulares")

        return entidad

    def clean_calendario(self):
        calendario = self.cleaned_data['calendario']
        if not calendario:
            raise forms.ValidationError("Este campo es requerido")

        consultorio = models.Consultorio.objects.first()
        if datetime.datetime.today().day + 1 is calendario.inicio.day:
            if consultorio:
                if consultorio.hora_maxima.hour >= datetime.datetime.today().hour:
                    raise forms.ValidationError("Por favor reserve para un dia posterior")
            elif 17 >= datetime.datetime.today().hour:
                raise forms.ValidationError("Por favor reserve para un dia posterior")

        if calendario.inicio.date() <= datetime.date.today():
            raise forms.ValidationError("No se pueden asignar citas para días anteriores a la fecha actual")

        return calendario
    # end def

    def save(self, commit=False):
        cita = super(CitaMedicaFormSupra, self).save(commit)
        if hasattr(self, 'instance') and self.instance.pk:
            cita.save()
        else:
            user = CuserMiddleware.get_user()
            paciente = models.Paciente.objects.filter(id=user.id).first()
            cita.paciente = paciente.id
            cita.save()
        # end if
        return cita
    # end if
# end class


class CancelarCitaForm(forms.ModelForm):

    class Meta:
        model = models.CitaCancelada
        exclude = ()
    # end class

    def clean(self):
        cleaned_data = super(CancelarCitaForm, self).clean()
        cita = self.cleaned_data.get("cita", False)
        if cita:
            if cita.procedimiento.modalidad == 2:
                raise forms.ValidationError("Solo se pueden cancelar las citas que son modo consultorio")
            # end if
    # end if
# end class
