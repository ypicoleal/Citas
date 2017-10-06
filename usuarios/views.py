# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import timedelta
from django.core.signing import TimestampSigner
from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponse
import models
import forms
from forms import ConfirmacionForm
from emails import emailConfirmation
from Citas.settings import ORIGIN
from supra import views as supra
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import login, logout, authenticate
import json

supra.SupraConf.ACCECC_CONTROL["allow"] = True
supra.SupraConf.ACCECC_CONTROL["origin"] = ORIGIN
supra.SupraConf.ACCECC_CONTROL["credentials"] = "true"
supra.SupraConf.ACCECC_CONTROL["headers"] = "origin, content-type, accept"
supra.SupraConf.ACCECC_CONTROL["methods"] = "POST, GET, PUT, DELETE ,OPTIONS"
supra.SupraConf.body = True
# Create your views here.

def confirmacion(request):
    key1 = request.GET.get('code', False)
    key2 = request.GET.get('k2', False)
    mensaje = ""
    if key1 and key2:
        activador = models.ActivacionUser.objects.filter(key1=key1, key2=key2).first()
        if activador:
            value = "%s:%s:%s" % (activador.email, activador.key1, activador.key2)
            signer = TimestampSigner()
            try:
                email = signer.unsign(value, max_age=timedelta(seconds=60))
                if activador.tipo == 1:
                    medico = models.Medico.objects.filter(email=email).first()
                    if medico:
                        medico.activado = True
                        medico.save()
                    # end if
                else:
                    paciente = models.Paciente.objects.filter(email=email).first()
                    if paciente:
                        paciente.activado = True
                        paciente.save()
                # end if
                mensaje = "Cuenta Activada"
            except:
                mensaje = "Esta URL a expirado"
            # end try
            activador.delete()
            return render(request, 'usuarios/confirmacion.html', {'mensaje': mensaje, 'nuevo': False})
        # end if
        mensaje = "Esta URL a expirado"
        return render(request, 'usuarios/confirmacion.html', {'mensaje': mensaje, 'nuevo': True})
    # end if
    return HttpResponseNotFound('<h1>Pagina no encontrada</h1>')
# end def

def generarConfirmacion(request):
    if request.POST:
        form = ConfirmacionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            paciente = models.Paciente.objects.filter(email=email).first()
            if paciente:
                emailConfirmation(email, 2)
            # end if
            medica = models.Medico.objects.filter(email=email).first()
            if medica:
                emailConfirmation(email, 1)
            # end if
            return render(request, 'usuarios/nuevaconfirmacion.html', {'form': ConfirmacionForm(), 'exito': True})
        # end if
        return render(request, 'usuarios/nuevaconfirmacion.html', {'form': form, 'exito': False})
    # end if
    return render(request, 'usuarios/nuevaconfirmacion.html', {'form': ConfirmacionForm(), 'exito': False})
# end def


class LoginU(supra.SupraSession):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        a = super(LoginU, self).dispatch(request, *args, **kwargs)
        return a
    # end def
# end class

class PacienteSupraForm(supra.SupraFormView):
    model = models.Paciente
    form_class = forms.PacienteFormService

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        a = super(PacienteSupraForm, self).dispatch(request, *args, **kwargs)
        return a
    # end def
# end class


@supra.access_control
def logoutUser(request):
    logout(request)
    return HttpResponse(status=200)
# end def

@supra.access_control
def islogin(request):
    if request.user.is_authenticated():
        return HttpResponse(json.dumps({"session": request.session.session_key, "username": request.user.username, "nombre": request.user.first_name, "apellido": request.user.last_name}), 200)
    # end if
    return HttpResponse([], 400)
# end if
