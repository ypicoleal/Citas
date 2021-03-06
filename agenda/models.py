# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from usuarios import models as usuarios
from djcelery.models import PeriodicTask, CrontabSchedule
import datetime
# Create your models here.


class Consultorio(models.Model):
    nombre = models.CharField(max_length=120)
    celular = models.CharField(
        max_length=15, verbose_name="Teléfono celular")
    direccion = models.CharField("Dirección", max_length=120)
    hora_maxima = models.TimeField("Hora máxima de reserva")
    nit = models.CharField(max_length=120)
    correo = models.EmailField()

    def __unicode__(self):
        return u"%s" % self.nombre
    # end def
# end class


class ProcedimientoMedico(models.Model):
    CONSULTORIO = 1
    VIRTUAL = 2
    choices = (
        (CONSULTORIO, 'Consultorio'),
        (VIRTUAL, 'Virtual')
    )
    nombre = models.CharField(max_length=120)
    precio = models.IntegerField(default=0, blank=True)
    modalidad = models.IntegerField(choices=choices)
    eliminado = models.BooleanField(default=False)

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
    admin = models.BooleanField(default=False)
    eliminado = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Calendario cita"
        verbose_name_plural = "Calendarios de cita"
    # end class

    def __unicode__(self):
        if self.almuerzo:
            fecha = u"Hora almuerzo %s %s" % (self.inicio.strftime('%Y-%m-%d %H:%M:%S'), self.fin.strftime('%H:%M:%S'))
        else:
            fecha = u"%s %s" % (self.inicio.strftime('%Y-%m-%d %H:%M:%S'), self.fin.strftime('%H:%M:%S'))
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
        (3, 'Vencida')
    )
    choices3 = (
        (1, 'Confirmado'),
        (2, 'Cancelado')
    )
    choices4 = (
        (1, "Mejoria"),
        (2, "Sin tiempo"),
        (3, "Otro motivo")
    )
    paciente = models.ForeignKey(usuarios.Paciente)
    procedimiento = models.ForeignKey(ProcedimientoMedico)
    entidad = models.IntegerField(choices=choices)
    estado = models.IntegerField("Estado cita", choices=choices2, default=1)
    confirmacion = models.IntegerField("Confirmación de cita", choices=choices3, blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    fecha_calendario = models.CharField(max_length=100, blank=True, null=True)
    calendario = models.OneToOneField(CalendarioCita, blank=True, null=True)
    cancelar = models.BooleanField("Cancelada", default=False)
    motivo = models.IntegerField("Motivo de cancelación", choices=choices4, blank=True, null=True)
    fecha_canelacion = models.DateTimeField("Fecha de cancelación", blank=True, null=True)
    eliminado = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Cita médica"
        verbose_name_plural = "Citas medicas"
    # end class

    def __unicode__(self):
        if self.cancelar:
            mensaje = u"%s - %s %s - Cancelado" % (self.procedimiento.nombre, self.paciente.first_name, self.paciente.last_name)
        else:
            mensaje = u"%s - %s %s - %s %s" % (self.procedimiento.nombre, self.paciente.first_name, self.paciente.last_name, self.calendario.inicio.strftime('%Y-%m-%d %H:%M:%S'), self.calendario.fin.strftime('%H:%M:%S'))
        return mensaje
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

    def save(self, *args, **kwargs):
        if self.calendario:
            self.fecha_calendario =  "%s %s" % (self.calendario.inicio.strftime('%Y-%m-%d %H:%M:%S'),  self.calendario.fin.strftime('%H:%M:%S'))
        # end if
        if self.confirmacion == 2:
            self.cancelar = True
            self.calendario = None
            self.estado = 2
            self.fecha_canelacion = datetime.date.today()
        super(CitaMedica, self).save(*args, **kwargs)
        obj  = PeriodicTask.objects.filter(
            name= "Prueba crontab %d" % (self.pk),
            task= "notificacion",
        )
        print "#######",self.pk, obj
        if not obj:
            crontab = CrontabSchedule(minute=1)
            crontab.save()
            obj  = PeriodicTask.objects.create(
                name= "Prueba crontab %d" % (self.pk),
                task= "notificacion",
                crontab= crontab,
                args = [self.pk]
            )
        else:
            obj.args = [self.pk]
            obj.save()
        print obj
# end class


class CitaReprogramada(models.Model):
    RESPONSABLE_MEDICO = False
    RESPONSABLE_PACIENTE = True

    choices = (
        (RESPONSABLE_MEDICO, "Medico"),
        (RESPONSABLE_PACIENTE, "Paciente")
    )
    cita = models.ForeignKey(CitaMedica)
    calendario = models.ForeignKey(CalendarioCita)
    motivo = models.TextField()
    responsable_cambio = models.BooleanField("Responsable del cambio", choices=choices, default=False)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Reprogramar cita"
        verbose_name_plural = "Reprogramar cita"
    # end class


    def __unicode__(self):
        return u"%s Reprogramado por  %s" % (self.cita, self.motivo)
    # end def
# end class


class DuracionCita(models.Model):
    cita = models.ForeignKey(CitaMedica)
    duracion_r = models.IntegerField("Minutos restantes")

    class  Meta:
        verbose_name = "Duración cita"
        verbose_name_plural = "Duración cita"
    # end class

    def __unicode__(self):
        return u"%s Minutos restantes %d" % (self.cita, self.duracion_r)
    # end def
# end class


class PagoCita(models.Model):
    cita = models.ForeignKey(CitaMedica)
    fecha = models.DateTimeField(auto_now_add=True)
# end class
