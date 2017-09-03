# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Medico(User):
    choices = (
        (1, 'Cédula'),
        (2, 'Pasaporte'),
        (3, 'Cédula de extranjeria')
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
        if self.tipo == 1:
            tipo = "Cédula"
        elif self.tipo == 2:
            tipo = "Pasaporte"
        else:
            tipo = "Cédula de extranjeria"
        # end if
        return tipo
    # end def
# end class


class Paciente(User):
    choices = (
        (1, 'Cédula'),
        (2, 'Tarjeta de identidad'),
        (3, 'Cédula de extranjeria'),
        (4, 'Registro Civil'),
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
        if self.tipo == 1:
            tipo = "Cédula"
        elif self.tipo == 2:
            tipo = "Tarjeta de identidad"
        elif self.tipo == 3:
            tipo = "Cédula de extranjeria"
        else:
            tipo = "Registro Civil"
        # end if
        return tipo
    # end def
# end class


class ActivacionUser(models.Model):
    choices = (
        (1, "Medico"),
        (2, "Paciente")
    )
    email = models.EmailField()
    key1 = models.CharField(max_length=100)
    key2 = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)
    tipo = models.IntegerField(choices=choices)
# end class
