# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import timedelta
from django.core.signing import TimestampSigner
from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponse
import models
import forms
from forms import ConfirmacionForm
from emails import emailConfirmation, emailComentarios
from Citas.decorator import check_login
from Citas.settings import ORIGIN
from supra import views as supra
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
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

    def get_form_class(self):
        if 'pk' in self.http_kwargs:
            self.form_class = forms.PacienteEdit
        # end if
        return self.form_class
    # end class
# end class

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
        paciente = models.Paciente.objects.filter(id=request.user.pk).first()
        if paciente:
            data = {"session": request.session.session_key, "username": request.user.username, "nombre": request.user.first_name, "apellidos": request.user.last_name, "id": request.user.pk, "tipo": 1 , "email": request.user.email}
        else:
            data = {"session": request.session.session_key, "username": request.user.username, "nombre": request.user.first_name, "apellidos": request.user.last_name, "id": request.user.pk, "tipo": 2 , "email": request.user.email}
        # end if
        return HttpResponse(json.dumps(data), 200)
    # end if
    return HttpResponse([], 400)
# end if

"""
    PasswordChange
"""
@check_login
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return HttpResponse(status=200)
        # end if
        errors = form.errors.items()
        return HttpResponse(json.dumps(errors), status=400, content_type='application/json')
    form = PasswordChangeForm(request.user)
    return render(request, 'usuarios/change_password.html', {'form': form})
    #end if
# end def

"""
    Forget Password
"""


def forget_password(request):
    if request.method == "POST":
        form = forms.ChangePasswordForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('newPassword2')
            u = User.objects.get(email=email)
            u.set_password(raw_password=password)
            u.save()
            return HttpResponse(status=200)
        # end if
        errors = form.errors.items()
        return HttpResponse(json.dumps(errors), status=400, content_type='application/json')
    # end if
    form = forms.ChangePasswordForm()
    return render(request, 'usuarios/change_password.html', {'form': form})
# end def


"""
    Comentarios
"""
def comentarios(request):
    if request.method == "POST":
        form = forms.ComentarioForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            comentario = request.POST.get('comentario')
            emailComentarios(email, comentario)
            return HttpResponse(status=200)
        # end if
        errors = form.errors.items()
        return HttpResponse(json.dumps(errors), status=400, content_type='application/json')
    # end if
    form = forms.ComentarioForm()
    return render(request, 'usuarios/comentarios.html', {'form': form})
# end def
