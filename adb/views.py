# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from supra import views as supra
from models import PublicidadMovil
from django.utils.decorators import method_decorator
from Citas.decorator import check_login
from Citas.settings import ORIGIN

supra.SupraConf.ACCECC_CONTROL["allow"] = True
supra.SupraConf.ACCECC_CONTROL["origin"] = ORIGIN
supra.SupraConf.ACCECC_CONTROL["credentials"] = "true"
supra.SupraConf.ACCECC_CONTROL["headers"] = "origin, content-type, accept"
supra.SupraConf.ACCECC_CONTROL["methods"] = "POST, GET, PUT, DELETE ,OPTIONS"
supra.SupraConf.body = True
# Create your views here.

class PublicidadMovilList(supra.SupraListView):
    model = PublicidadMovil
    list_display = ['url', 'img']
    paginate_by = 10

    @method_decorator(check_login)
    def dispatch(self, request, *args, **kwargs):
        return super(PublicidadMovilList, self).dispatch(request, *args, **kwargs)
    # end def

    def img(self, obj, row):
        if obj.imagen:
            return "/media/%s" % (obj.imagen)
        # end if
        return None
    # end def
# end class
