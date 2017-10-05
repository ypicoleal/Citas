# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
import models as usuarios
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Permission, Group
from emails import emailConfirmation


class ConfirmacionForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data['email']
        if email:
            user = usuarios.User.objects.filter(email=email).first()
            if not user:
                raise forms.ValidationError("No existe ningún usuario con este correo")
            # end if
            return email
        # end if
        raise forms.ValidationError("Este campo es requerido")
    # end def
# end def

class MedicoForm(forms.ModelForm):
    identificacion2 = forms.CharField(widget=forms.NumberInput() , label="Verificar número identificación")

    def clean_identificacion(self):
        identificacion = self.cleaned_data['identificacion']
        if identificacion:
            user = User.objects.filter(username=identificacion).first()
            medico = usuarios.Medico.objects.filter(identificacion=identificacion).first()
            if hasattr(self, 'instance') and self.instance.pk:
                if user.id != self.instance.id:
                    raise forms.ValidationError('Ya existe un usuario con este username')
                # end if
                if medico != self.instance:
                    raise forms.ValidationError('Ya existe un usuario con esta identificación')
                # end if
                return identificacion
            else:
                if user:
                    raise forms.ValidationError('Ya existe un usuario con este username')
                # end if
                if medico:
                    raise forms.ValidationError('Ya existe un usuario con esta identificación')
                # end if
                return identificacion
        # end if
        raise forms.ValidationError('Este campo es requerido')
    # end def

    def clean_identificacion2(self):
        identificacion = self.cleaned_data.get('identificacion', False)
        identificacion2 = self.cleaned_data.get('identificacion2', False)
        if identificacion2:
            if identificacion2 == identificacion:
                return identificacion
            else:
                raise forms.ValidationError("Los números de identificación no coinciden")
            # end if
        else:
            raise forms.ValidationError("Este campo es requerido")
        # end if

    # end def

    def __init__(self, *args, **kwargs):
        super(MedicoForm, self).__init__(*args, **kwargs)
        if hasattr(self, 'instance') and self.instance.pk:
            self.fields['identificacion2'].initial = self.instance.identificacion
        # end if
    # end def

    class Meta:
        model = usuarios.Medico
        fields = ['first_name', 'last_name', 'email', 'tipo', 'identificacion', 'identificacion2',
                  'fecha_nacimiento', 'numero_registro', 'nombre_u', 'telefono', 'especialidad']
        widgets = {
            'identificacion': forms.NumberInput(),
            'telefono': forms.NumberInput()
        }

    def save(self, commit=False):
        medico = super(MedicoForm, self).save(commit)
        emailConfirmation(medico.email, 1)
        # end if
        medico.is_staff = True
        medico.username = medico.identificacion
        medico.set_password(raw_password=medico.identificacion)

        grupo, created = Group.objects.get_or_create(name="Medico")
        if created:
            permisos = Permission.objects.all().exclude(codename__contains="log").exclude(codename__contains="group").exclude(codename__contains="permission").exclude(codename__contains="user").exclude(codename__contains="content type").exclude(codename__contains="session")
            grupo.permissions.set(permisos)
        medico.save()
        medico.groups.add(grupo)
        return medico
    # end def
# end class

class PacienteAdmin(forms.ModelForm):

    identificacion2 = forms.CharField(widget=forms.NumberInput() , label="Verificar número identificación")

    def clean_identificacion(self):
        identificacion = self.cleaned_data['identificacion']
        if identificacion:
            user = User.objects.filter(username=identificacion).first()
            paciente = usuarios.Paciente.objects.filter(identificacion=identificacion).first()
            if hasattr(self, 'instance') and self.instance.pk:
                if user.id != self.instance.id:
                    raise forms.ValidationError('Ya existe un usuario con este username')
                # end if
                if paciente != self.instance:
                    raise forms.ValidationError('Ya existe un usuario con esta identificación')
                # end if
                return identificacion
            else:
                if user:
                    raise forms.ValidationError('Ya existe un usuario con este username')
                # end if
                if paciente:
                    raise forms.ValidationError('Ya existe un usuario con esta identificación')
                # end if
                return identificacion
        # end if
        raise forms.ValidationError('Este campo es requerido')
    # end def

    def clean_identificacion2(self):
        identificacion = self.cleaned_data.get('identificacion', False)
        identificacion2 = self.cleaned_data.get('identificacion2', False)
        if identificacion2:
            if identificacion2 == identificacion:
                return identificacion
            else:
                raise forms.ValidationError("Los números de identificación no coinciden")
            # end if
        else:
            raise forms.ValidationError("Este campo es requerido")
        # end if
    # end def

    def __init__(self, *args, **kwargs):
        super(PacienteAdmin, self).__init__(*args, **kwargs)
        if hasattr(self, 'instance') and self.instance.pk:
            self.fields['identificacion2'].initial = self.instance.identificacion
            if self.instance.nombre_a:
                self.fields['nombre_a'].widget.attrs['disabled'] = False
            if self.instance.cedula_a:
                self.fields['cedula_a'].widget.attrs['disabled'] = False
        else:
            self.fields['nombre_a'].widget.attrs['disabled'] = True
            self.fields['cedula_a'].widget.attrs['disabled'] = True
        # end if


    # end def

    class Meta:
        model = usuarios.Paciente
        fields = ['first_name', 'last_name', 'email', 'tipo', 'identificacion', 'identificacion2',
                  'fecha_nacimiento', 'estado_civil', 'profesion', 'telefono', 'nombre_a', 'cedula_a']
        widgets = {
            'identificacion': forms.NumberInput(),
            'telefono': forms.NumberInput()
        }

    def save(self, commit=False):
        paciente = super(PacienteAdmin, self).save(commit)
        paciente.username = paciente.identificacion
        paciente.activado = True
        paciente.set_password(raw_password=paciente.identificacion)
        paciente.save()
        return paciente
    # end def
# end class


class PacienteFormService(UserCreationForm):

    class Meta:
        model = usuarios.Paciente
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'tipo',
                  'identificacion', 'fecha_nacimiento', 'estado_civil', 'profesion', 'telefono', 'nombre_a', 'cedula_a']

        widgets = {
            'identificacion': forms.NumberInput(),
            'telefono': forms.NumberInput()
        }

    def save(self, commit=True):
        paciente = super(PacienteFormService, self).save(commit)
        emailConfirmation(paciente.email, 2)
        return paciente
    # end def
# end class
