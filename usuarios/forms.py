# -*- coding: utf-8 -*-
from django import forms
import models as usuarios


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

    class Meta:
        model = usuarios.Medico
        fields = ['first_name', 'last_name', 'email', 'tipo', 'identificacion',
                  'fecha_nacimiento', 'numero_registro', 'nombre_u', 'telefono', 'especialidad']

    def save(self, commit=False):
        medico = super(MedicoForm, self).save(commit)
        medico.is_staff = True
        medico.username = medico.identificacion
        medico.set_password(raw_password=medico.identificacion)
        medico.save()
        return medico
    # end def
# end class
