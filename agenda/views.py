# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from supra import views as supra
from django.utils.decorators import method_decorator
from Citas.decorator import check_login
from django.views.decorators.csrf import csrf_exempt
import models
import forms
supra.SupraConf.body = True
# Create your views here.

class CalendarioCitaList(supra.SupraListView):
    model = models.CalendarioCita
    list_display = ['id', 'title', 'start', 'end', 'almuerzo']
    list_filter = ['inicio__year', 'inicio__month']

    def title(self, obj, row):
        return "Espacio para cita"

    def start(self, obj, row):
        return obj.inicio.strftime('%Y-%m-%d %H:%M:%S')

    def end(self, obj, now):
        return obj.fin.strftime('%Y-%m-%d %H:%M:%S')

    @method_decorator(check_login)
    def dispatch(self, request, *args, **kwargs):
        return super(CalendarioCitaList, self).dispatch(request, *args, **kwargs)



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


class CalandarioCitaDelete(supra.SupraFormView):
    model = models.CalendarioCita

    @method_decorator(check_login)
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(CalandarioCitaDelete, self).dispatch(request, *args, **kwargs)
    # end def
# end class
