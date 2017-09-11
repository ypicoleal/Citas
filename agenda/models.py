# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from usuarios import models as usuarios
# Create your models here.


class Consultorio(models.Model):
    nombre = models.CharField(max_length=120)
    celular = models.CharField(
        max_length=15, verbose_name="Teléfono celular")
    direccion = models.CharField("Dirección", max_length=120)
    nit = models.CharField(max_length=120)
    correo = models.EmailField()

    def __unicode__(self):
        return u"%s" % self.nombre
    # end def
# end class


class ProcedimientoMedico(models.Model):
    choices = (
        (1, 'Consultorio'),
        (2, 'Virtual')
    )
    nombre = models.CharField(max_length=120)
    precio = models.IntegerField(default=0, blank=True)
    modalidad = models.IntegerField(choices=choices)

    class Meta:
        verbose_name = "Procedimiento médico"
        verbose_name_plural = "Procedimientos médicos"
    # end class

    def __unicode__(self):
        return u"%s" % self.nombre
    # end def
# end class


class CalendarioCita(models.Model):
    inicio = models.DateTimeField()
    fin = models.DateTimeField()
    almuerzo = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Calendario cita"
        verbose_name_plural = "Calendarios de cita"
    # end class

    def __unicode__(self):
        if self.almuerzo:
            fecha = u"Hora almuerzo %s %s" % (self.inicio.strftime('%Y-%m-%d %H:%M:%S'), self.fin.strftime('%Y-%m-%d %H:%M:%S'))
        else:
            fecha = u"%s %s" % (self.inicio.strftime('%Y-%m-%d %H:%M:%S'), self.fin.strftime('%Y-%m-%d %H:%M:%S'))
        return fecha
# end class


class CitaMedica(models.Model):
    choices = (
        (1, 'Particular'),
        (2, 'Medisanitas'),
        (3, 'Colsanitas')
    )
    choices2 = (
        (1, 'Vigente'),
        (2, 'Cancelada'),
        (3, 'Vencida'),
        (4, 'Asistida')
    )
    choices3 = (
        (1, 'Confirmado'),
        (2, 'Cancelado')
    )

    paciente = models.ForeignKey(usuarios.Paciente)
    procedimiento = models.ForeignKey(ProcedimientoMedico)
    entidad = models.IntegerField(choices=choices)
    reprogramar = models.BooleanField(default=False)
    cancelar = models.BooleanField(default=False)
    estado = models.IntegerField("Estado cita", choices=choices2, default=1)
    confirmacion = models.IntegerField("Confirmación de cita", choices=choices3, blank=True, null=True)

    class Meta:
        verbose_name = "Cita médica"
        verbose_name_plural = "Citas medicas"
    # end class

    def __unicode__(self):
        return u"%s - %s %s - %s %s" % (self.procedimiento.nombre, self.paciente.first_name, self.paciente.last_name, self.inicio.strftime('%Y-%m-%d %H:%M:%S'), self.fin.strftime('%Y-%m-%d %H:%M:%S'))
    # end def

    def get_entidad(self):
        if self.entidad == 1:
            entidad = "Particular"
        elif self.entidad == 2:
            entidad = "Medisanitas"
        else:
            entidad = "Colsanitas"
        # end if
        return entidad
    # end def
# end def

class AsignacionCita(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    cita  = models.ForeignKey(CitaMedica)
    calendario = models.ForeignKey(CalendarioCita)
    cancelado = models.BooleanField()
# end class


class CitaReprogramada(models.Model):
    choices = (
        (False, "Medico"),
        (True, "Paciente")
    )
    cita = models.ForeignKey(AsignacionCita)
    motivo = models.TextField()
    responsable_cambio = models.BooleanField("Responsable del cambio", choices=choices)

    class Meta:
        verbose_name = "Cita reprogramada"
        verbose_name_plural = "Citas reprogramadas"
    # end class

    def __unicode__(self):
        return u"%s %s" % (self.cita, motivo)
    # end def
# end class

class CitaCancelada(models.Model):
    choices = (
        (1, "Mejoria"),
        (2, "Sin tiempo"),
        (3, "Otro motivo")
    )
    cita = models.ForeignKey(AsignacionCita)
    motivo = models.IntegerField(choices=choices)

    class Meta:
        verbose_name = "Cita cancelada"
        verbose_name_plural = "Citas canceladas"
    # end class

    def __unicode__(self):
        return u"%s %s" % (self.cita, motivo)
    # end def
# end class

class DuracionCita(models.Model):
    cita = models.ForeignKey(CitaMedica)
    duracion_r = models.IntegerField("Minutos restantes")

    class  Meta:
        verbose_name = "Duración cita"
        verbose_name_plural = "Duraciones de citas"
    # end class

    def __unicode__(self):
        return u"%s Minutos restantes %d" % (self.cita, duracion_r)
    # end def
# end class


class PagoCita(models.Model):
    cita = models.ForeignKey(CitaMedica)
    fecha = models.DateTimeField(auto_now_add=True)
# end class
