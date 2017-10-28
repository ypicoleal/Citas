# -*- coding: utf-8 -*-
import models
import datetime
import calendar
from django import forms
from django.db.models import Q
from usuarios import models as usuarios
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

    def rm_add_and_change_related(self):
        calendario = self.fields['calendario']
        calendario.widget.can_add_related = False
        calendario.widget.can_change_related = False

        procedimiento = self.fields['procedimiento']
        procedimiento.widget.can_add_related = False
        procedimiento.widget.can_change_related = False
    # end def

    def __init__(self, *args, **kwargs):
        super(CitaMedicaForm, self).__init__(*args, **kwargs)
        if hasattr(self, 'instance') and self.instance.pk:
            fecha = self.fields['fecha_']
            fecha.required = False
            fecha.widget.attrs['disabled'] = True
            if self.instance.procedimiento.modalidad == 2:
                CHOICES = (
                    (1, 'Vigente'),
                    (3, 'Vencida')
                )
                self.fields["estado"].widgets = forms.Select(choices=CHOICES)
            else:
                if self.instance.confirmacion != 2:
                    self.fields["motivo"].widget.attrs['disabled'] = True
                # end if
            # end if
        else:
            hoy = datetime.date.today()
            calendario = self.fields['calendario']
            calendario.queryset = models.CalendarioCita.objects.filter(inicio__year=hoy.year, inicio__month=hoy.month, citamedica=None)
            calendario.widget.attrs['disabled'] = True

            motivo = self.fields['motivo']
            motivo.widget.attrs['disabled'] = True

            procedimiento = self.fields['procedimiento']
            procedimiento.queryset = models.ProcedimientoMedico.objects.filter(modalidad=1, eliminado=False)
            paciente = self.fields['paciente']
            paciente.queryset = usuarios.Paciente.objects.filter(eliminado=False)
            self.rm_add_and_change_related()

    # end def
    class Meta:
        model = models.CitaMedica
        fields = ['paciente', 'procedimiento', 'entidad', 'fecha_', 'calendario', 'confirmacion', 'motivo', 'estado']

    def clean_entidad(self):
        entidad = self.cleaned_data.get('entidad', False)
        calendario = self.cleaned_data.get('calendario', False)
        if not entidad:
            raise forms.ValidationError("Este campo es requerido")

        if calendario:
            if calendario.inicio.weekday() is 4 and calendario.inicio.hour >= 13 and entidad != 1:
                raise forms.ValidationError("Lo sentimos. Solo hay disponibilidad de citas para particulares")
            elif calendario.inicio.weekday() is 5 and entidad != 1:
                raise forms.ValidationError("Lo sentimos. Solo hay disponibilidad de citas para particulares")

        return entidad
    # end def

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
        super(CitaMedicaFormSupra, self).clean()
        if not hasattr(self, 'instance'):
            user = CuserMiddleware.get_user()
            paciente = usuarios.Paciente.objects.filter(id=user.id).first()
            if not paciente:
                raise form.ValidationError("Necesita ser un paciente para crear una cita")
        # end if
    # end def

    def clean_entidad(self):
        entidad = self.cleaned_data.get('entidad', False)
        calendario = self.cleaned_data.get('calendario', False)
        if not entidad:
            raise forms.ValidationError("Este campo es requerido")

        if calendario:
            if calendario.inicio.weekday() is 4 and calendario.inicio.hour >= 13 and entidad != 1:
                raise forms.ValidationError("Lo sentimos. Solo hay disponibilidad de citas para particulares")
            elif calendario.inicio.weekday() is 5 and not entidad != 1:
                raise forms.ValidationError("Lo sentimos. Solo hay disponibilidad de citas para particulares")

        return entidad

    def clean_calendario(self):
        calendario = self.cleaned_data.get('calendario', False)
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
            paciente = usuarios.Paciente.objects.filter(id=user.id).first()
            cita.paciente = paciente
            cita.save()
        # end if
        return cita
    # end if
# end class


class CancelarCitaForm(forms.ModelForm):

    class Meta:
        model = models.CitaMedica
        fields = ('motivo', )
    # end class

    def clean(self):
        cleaned_data = super(CancelarCitaForm, self).clean()
        if hasattr(self, 'instance') and self.instance.pk:
            if self.instance.procedimiento.modalidad == 2:
                raise forms.ValidationError("Solo se pueden cancelar las citas que son de modalidad consultorio")
            # end if
    # end if

    def save(self, commit=True):
        cita = super(CancelarCitaForm, self).save(commit)
        obj = models.CitaMedica.objects.filter(id=cita.id).first()
        obj.cancelar = True
        obj.calendario = None
        obj.estado = 2
        obj.confirmacion = 2
        obj.fecha_canelacion = datetime.date.today()
        obj.save()
        return cita
# end class


class ReprogramarCitaForm(forms.ModelForm):
    fecha_ = forms.DateField(label="Filtro de fecha", required=False)

    class Meta:
        model = models.CitaReprogramada
        fields = ('fecha_', 'calendario', 'motivo')
    # end class

    def __init__(self, *args, **kwargs):
        super(ReprogramarCitaForm, self).__init__(*args, **kwargs)
        fecha = self.fields["fecha_"]
        if hasattr(self, 'instance') and self.instance.pk:

            if 'calendario' in self.fields:
                calendario = self.fields["calendario"]
                calendario.queryset = models.CalendarioCita.objects.filter(id=self.instance.calendario.id)
                calendario.widget.can_add_related = False
                calendario.widget.can_change_related = False
                #fecha.initial = self.instance.calendario.inicio.strftime('%d/%m/%Y')
                #self.fields["motivo"].widget.attrs['disabled'] = True
            # end if

                fecha.widget.attrs['disabled'] = True

        else:
            if 'calendario' in self.fields:
                hoy = datetime.date.today()
                calendario = self.fields['calendario']
                calendario.queryset = models.CalendarioCita.objects.filter(inicio__year=hoy.year, inicio__month=hoy.month, citamedica=None)
                # calendario.widget.attrs['disabled'] = True
                calendario.widget.can_add_related = False
                calendario.widget.can_change_related = False
            else:
                fecha.widget.attrs['disabled'] = True
            # end if
        # end if
    # end def

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

            cita = self.instance.cita
            if cita:
                entidad = cita.entidad
                if calendario.inicio.weekday() is 4 and calendario.inicio.hour >= 13 and entidad != 1:
                    raise forms.ValidationError("Lo sentimos. Solo hay disponibilidad de citas para particulares")
                elif calendario.inicio.weekday() is 5 and not entidad != 1:
                    raise forms.ValidationError("Lo sentimos. Solo hay disponibilidad de citas para particulares")
                # end if
                obj = models.CitaMedica.objects.filter(calendario=calendario).first()
                if obj:
                    if cita.id != obj.id:
                        raise forms.ValidationError("Ya este espacio esta ocupado por otra cita")
                # end if
            return calendario
        else:
            raise forms.ValidationError("Este campo es requerido")
    # end def

    def save(self, commit=False):
        programacion = super(ReprogramarCitaForm, self).save(commit)
        user = CuserMiddleware.get_user()
        paciente = usuarios.Paciente.objects.filter(id=user.id).first()
        if paciente:
            programacion.responsable_cambio = True
        # end if
        cita = models.CitaMedica.objects.filter(id=programacion.cita.id).first()
        cita.calendario = programacion.calendario
        cita.save()
        programacion.save()
        return programacion
# end class


class ReprogramarCitaFormSupra(forms.ModelForm):
    fecha_ = forms.DateField(label="Filtro de fecha", required=False)

    class Meta:
        model = models.CitaReprogramada
        fields = ('fecha_', 'calendario', 'motivo')
    # end class


    def __init__(self, *args, **kwargs):
        super(ReprogramarCitaFormSupra, self).__init__(*args, **kwargs)
        hoy = datetime.date.today()
        calendario = self.fields['calendario']
        calendario.queryset = models.CalendarioCita.objects.filter(inicio__year=hoy.year, inicio__month=hoy.month, )
    # end def

    def clean(self):
        cleaned_data = super(ReprogramarCitaFormSupra, self).clean()
        cita = self.cleaned_data.get('cita', False)
        if cita:
            reprogramaciones = models.CitaReprogramada.objects.filter(cita=cita).count()
            if reprogramaciones == 3:
                raise forms.ValidationError("No se puede reprogramar una cita mas de 3 veces.")
            # end if
        # end if
    # end def

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
                return self.instance.calendario
            # end if
            raise forms.ValidationError("Este campo es requerido")
    # end def

    def save(self, commit=False):
        programacion = super(ReprogramarCitaFormSupra, self).save(commit)
        user = CuserMiddleware.get_user()
        paciente = usuarios.Paciente.objects.filter(id=user.id).first()
        if paciente:
            programacion.responsable_cambio = True
        # end if
        cita = models.CitaMedica.objects.filter(id=programacion.cita.id).first()
        cita.calendario = programacion.calendario
        cita.save()
        programacion.save()
        return programacion
# end class


class ConfirmacionPago(forms.ModelForm):

    class Meta:
        model = models.PagoCita
        exclude = ('cita', )
    # end class
# end class
