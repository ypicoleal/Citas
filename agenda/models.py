# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from usuarios import models as usuarios
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
    precio = models.IntegerField("Precio COP", default=0, blank=True)
    precio_usd = models.IntegerField("Precio USD", default=0, blank=True)
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
    virtual = models.BooleanField(default=False)
    pago = models.BooleanField(default=False)

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
        if self.procedimiento.modalidad == 2:
            self.confirmacion = 1
        else:
            if self.confirmacion == 2:
                self.cancelar = True
                self.calendario = None
                self.estado = 2
                self.fecha_canelacion = datetime.date.today()
        super(CitaMedica, self).save(*args, **kwargs)
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
    merchantId = models.IntegerField()
    state_pol = models.CharField("Indica el estado de la transacción en el sistema.", max_length=32, blank=True, null=True)
    response_code_pol = models.CharField("Codigo de respuesta de PayU.", max_length=255)
    response_message_pol = models.CharField("Mensaje de respuesta de PAYU.", max_length=255)
    reference_sale = models.CharField("Es la referencia de la venta o pedido.", max_length=255)
    reference_pol = models.CharField("Referencia o número de la transacción generado en PayU.", max_length=255)
    sign = models.CharField("Firma digital creada para cada uno de las transacciones.", max_length=255)
    extra1 = models.CharField("Campo adicional para enviar información sobre la compra", max_length=255, blank=True, null=True)
    extra2 = models.CharField("Campo adicional para enviar información sobre la compra", max_length=255, blank=True, null=True)
    extra3 = models.CharField("Campo adicional para enviar información sobre la compra", max_length=255, blank=True, null=True)
    payment_method = models.IntegerField("Identificador interno del medio de pago utilizado.")
    payment_method_type = models.IntegerField("Tipo de medio de pago utilizado para el pago")
    installments_number = models.IntegerField("Número de cuotas en las cuales se difirió el pago con tarjeta crédito.")
    value = models.DecimalField("Monto total de la transacción", max_digits=19, decimal_places=2, blank=True, null=True)
    tax = models.IntegerField()
    additional_value = models.DecimalField(max_digits=19, decimal_places=2)
    transaction_date = models.CharField("Fecha en que se realizó la transacción.", max_length=50)
    currency = models.CharField(max_length=3)
    email_buyer = models.CharField(max_length=255)
    cus = models.CharField("Código único de seguimiento", max_length=64)
    pse_bank = models.CharField("Nombre del banco, aplica solo para pagos con PSE.", max_length=255)
    test = models.IntegerField()
    description = models.CharField(max_length=255)
    billing_address = models.CharField("La dirección de facturación", max_length=255, blank=True, null=True)
    shipping_address = models.CharField("La dirección de entrega de la mercancía.", max_length=55, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    office_phone = models.CharField(max_length=20, blank=True, null=True)
    account_number_ach = models.CharField("Identificador de la transacción.", max_length=36, blank=True, null=True)
    account_type_ach  models.CharField("Identificador de la transacción.", max_length=36, blank=True, null=True)
    administrative_fee  = models.DecimalField("Valor de la tarifa administrativa", max_digits=19, decimal_places=2)
    administrative_fee_base = models.DecimalField("Valor base de la tarifa administrativa", max_digits=19, decimal_places=2)
    administrative_fee_tax = models.DecimalField("Valor del impuesto de la tarifa administrativa", max_digits=19, decimal_places=2)
    airline_code = models.CharField("Código de la aerolínea", max_length=4, blank=True, null=True)
    attempts = model.IntegerField("Numero de intentos del envío de la confirmación.")
    authorization_code = models.CharField("Código de autorización de la venta", max_length=12, blank=True, null=True)
    bank_id = models.CharField("Identificador del banco", max_length=255)
    billing_city = models.CharField("La ciudad de facturación.", max_length=255)
    billing_country = models.CharField("El código ISO del país asociado a la dirección de facturación.", max_length=2)
    commision_pol =  models.DecimalField("Valor de la comisión", max_digits=19, decimal_places=2, blank=True, null=True)
    commision_pol_currency = models.CharField("Moneda de la comisión", max_length=3, blank=True, null=True)
    customer_number = models.IntegerField("Numero de cliente.", blank=True, null=True)
    date = models.CharField("Fecha de la operación.", max_length=255)
    error_code_bank = models.CharField("Código de error del banco.", max_length=255, blank=True, null=True)
    error_message_bank = models.CharField("Mensaje de error del banco", max_length=255, blank=True, null=True)
    exchange_rate = models.DecimalField("Valor de la tasa de cambio.",  max_digits=19, decimal_places=2, blank=True, null=True)
    ip = models.CharField("Dirección ip desde donde se realizó la transacción.", max_length=39)
    nickname_buyer = models.CharField("Nombre corto del comprador.", max_length=150, blank=True, null=True)
    nickname_seller = models.CharField("Nombre corto del vendedor.", max_length=150, blank=True, null=True)
    payment_method_id = models.IntegerField("Identificador del medio de pago.")
    payment_request_state = models.CharField("Estado de la solicitud de pago.", max_length=30)
    pseReference1 = models.CharField("Referencia no. 1 para pagos con PSE.", max_length=255, blank=True, null=True)
    pseReference2 = models.CharField("Referencia no. 2 para pagos con PSE.", max_length=255, blank=True, null=True)
    pseReference3 = models.CharField("Referencia no. 3 para pagos con PSE.", max_length=255, blank=True, null=True)
    response_message_pol = models.CharField("El mensaje de respuesta de PAYU.", max_length=255)
    shipping_city = models.CharField("La ciudad de entrega de la mercancía.", max_length=255, blank=True, null=True)
    shipping_country = models.CharField("El código ISO asociado al país de entrega de la mercancía.", max_length=2, blank=True, null=True)
    transaction_bank_id = models.CharField("Identificador de la transacción en el sistema del banco.", max_length=255, blank=True, null=True)
    transaction_id = models.CharField("Identificador de la transacción.", max_length=255)
    payment_method_name = models.CharField("Medio de pago con el cual se hizo el pago.", max_length=255)
# end class
