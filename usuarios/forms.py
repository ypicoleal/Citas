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
    identificacion2 = forms.CharField(widget=forms.NumberInput() , label="Verificar número identificación")

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
        medico.is_staff = True
        medico.username = medico.identificacion
        medico.set_password(raw_password=medico.identificacion)
        medico.save()
        return medico
    # end def
# end class
