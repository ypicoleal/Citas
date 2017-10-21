# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Medico(User):
    CEDULA = 1
    PASAPORTE = 2
    C_EXTRANJERIA = 3
    choices = (
        (CEDULA, 'Cédula'),
        (PASAPORTE, 'Pasaporte'),
        (C_EXTRANJERIA, 'Cédula de extranjeria')
    )
    tipo = models.IntegerField("Tipo de identificación", choices=choices)
    identificacion = models.CharField(
        "N° de indentificación", max_length=120, unique=True)
    fecha_nacimiento = models.DateField()
    numero_registro = models.CharField(
        "N° registro profesional", max_length=120)
    nombre_u = models.CharField("Nombre de universidad", max_length=120)
    telefono = models.CharField(
        max_length=15, verbose_name="Teléfono celular")
    especialidad = models.CharField(max_length=120)
    activado = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Médico"
        verbose_name_plural = "Médicos"
    # end class

    def __unicode__(self):
        return u"%s %s"%(self.first_name, self.last_name)
    # end def

    def _tipo(self):
        if self.tipo == self.CEDULA:
            tipo = "Cédula"
        elif self.tipo == self.PASAPORTE:
            tipo = "Pasaporte"
        else:
            tipo = "Cédula de extranjeria"
        # end if
        return tipo
    # end def
# end class


class Paciente(User):
    CEDULA = 1
    T_IDENTIDAD = 2
    C_EXTRANJERIA = 3
    REGISTROCIVIL = 4
    choices = (
        (CEDULA, 'Cédula'),
        (T_IDENTIDAD, 'Tarjeta de identidad'),
        (C_EXTRANJERIA, 'Cédula de extranjeria'),
        (REGISTROCIVIL, 'Registro Civil'),
    )
    tipo = models.IntegerField("Tipo de identificación", choices=choices)
    identificacion = models.CharField(
        "Número de indentificación", max_length=120, unique=True)
    fecha_nacimiento = models.DateField()
    estado_civil = models.CharField(max_length=120)
    profesion = models.CharField("Profesión", max_length=120, blank=True, null=True)
    nombre_a = models.CharField("Nombre completo acudiente", max_length=120, blank=True, null=True)
    cedula_a = models.CharField("Cedula acudiente", max_length=120, blank=True, null=True)
    telefono = models.CharField("Teléfono celular", max_length=15, blank=True, null=True)
    activado = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
    # end class


    def __unicode__(self):
        return u"%s %s"%(self.first_name, self.last_name)
    # end def

    def _tipo(self):
        if self.tipo == self.CEDULA:
            tipo = "Cédula"
        elif self.tipo == self.T_IDENTIDAD:
            tipo = "Tarjeta de identidad"
        elif self.tipo == self.C_EXTRANJERIA:
            tipo = "Cédula de extranjeria"
        else:
            tipo = "Registro Civil"
        # end if
        return tipo
    # end def
# end class


class ActivacionUser(models.Model):
    MEDICO = 1
    PACIENTE = 2
    choices = (
        (MEDICO, "Medico"),
        (PACIENTE, "Paciente")
    )
    email = models.EmailField()
    key1 = models.CharField(max_length=100)
    key2 = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)
    tipo = models.IntegerField(choices=choices)
# end class
