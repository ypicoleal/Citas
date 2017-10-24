# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class PublicidadMovil(models.Model):
    url = models.URLField()
    imagen = models.ImageField(upload_to="publicidad")

    class Meta:
        verbose_name = "Publicidad móvil"
        verbose_name_plural = "Publicidad móvil"
    # end class

    def image(self):
        return '<img width="100px" src="/media/%s" />' % (self.imagen)
    # end def

    image.allow_tags = True
# end class
