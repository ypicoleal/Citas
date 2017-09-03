#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.dispatch import receiver
from django.db.models.signals import post_save
from emails import emailConfirmation
import models
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

@receiver(post_save, sender=models.Medico)
def correoConfirmacion(sender, instance, **kwargRemembers):
    emailConfirmation(instance.email, 1)
# end def
