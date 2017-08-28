#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
    subject, from_email, to = "Confirmar cuenta", 'mariobarrios@gmail.com', [email]
    text_content = "Confirmación de cuenta"
    html_content = "Enlace de confirmacion: http://127.0.0.1:8000/usuarios/confirmacion/?code=%s&k2=%s" % (key1, key2)
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(unicode(html_content, encoding='utf-8'), "text/html")
    msg.send()
# end def
