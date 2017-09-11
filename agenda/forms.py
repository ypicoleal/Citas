# -*- coding: utf-8 -*-
from django import forms
from django.db.models import Q
import models
import datetime

def getTimeDifference(TimeStart, TimeEnd):
    timeDiff = TimeEnd - TimeStart
    return timeDiff.total_seconds() / 60

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
            calendario = models.CalendarioCita.objects.filter(inicio=inicio, fin=fin).first()
            if calendario:
                raise forms.ValidationError("Ya existe una cita en ese este rango de fechas")
        if inicio:
            if inicio.date() <= hoy:
                raise forms.ValidationError("Solo puede crear calendarios para dias futuros")

    def clean_fin(self):
        fin = self.cleaned_data['fin']
        inicio = self.cleaned_data.get('inicio', False)
        if fin:
            if inicio:
                if inicio >= fin:
                    raise forms.ValidationError("Fin debe ser mayor a inicio")
                elif getTimeDifference(inicio, fin) > 30:
                    raise forms.ValidationError("El rango de fecha no puede superar los 30 minutos")

            return fin
        else:
            raise forms.ValidationError("Este campo es requerido")

class CalendarioCitaFormEdit(forms.ModelForm):

    class Meta:
        model = models.CalendarioCita
        exclude = ('inicio', 'fin')
