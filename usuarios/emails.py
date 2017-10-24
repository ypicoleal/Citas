# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.mail import EmailMultiAlternatives

from datetime import timedelta
from django.core.signing import TimestampSigner
import models

def emailConfirmation(email, tipo):
    signer = TimestampSigner()
    value = signer.sign(email)
    key1 = value.split(':')[1]
    key2 = value.split(':')[2]
    activacionkey = models.ActivacionUser(email=email, key1=key1, key2=key2, tipo=tipo)
    activacionkey.save()
    subject, from_email, to = "Confirmar cuenta", 'info@dranilsaarias.com', [email]
    text_content = "Confirmación de cuenta"
    html_content = "Enlace de confirmacion: http://app.dranilsaarias.com/usuarios/confirmacion/?code=%s&k2=%s" % (key1, key2)
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
# end def


def emailComentarios(email, comentario):
    medicos = models.Medico.objects.all()
    paciente = models.Paciente.objects.filter(email=email).first()
    if paciente:
        nombre = "%s %s" % (paciente.first_name, paciente.last_name)
    else:
        nombre = "Anónimo"
    # end def
    emails = []
    for m in medicos:
        emails.append(m.email)
    # end for
    if not len(emails):
        emails.append("info@dranilsaarias.com")
    # end if
    subject, from_email, to = "Comentarios", 'info@dranilsaarias.com', emails
    text_content = "Comentario enviado %s" % (nombre)
    html_content = "<p>Correo del emisor: %s</p><p>%s</p>" % (email, comentario)
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
# end def
