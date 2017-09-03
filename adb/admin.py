# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
import models
# Register your models here.

@admin.register(models.PublicidadMovil)
class PublicidadAdmin(admin.ModelAdmin):
    list_display = ('url', 'imagen')
    search_fields = ('url', )
# end class
