from django.http import HttpResponse
import json as simplejson
from supra import views as supra
from Citas.settings import ORIGIN
from usuarios.models import Medico, Paciente

# Create your views here.
supra.SupraConf.ACCECC_CONTROL["allow"] = True
supra.SupraConf.ACCECC_CONTROL["origin"] = ORIGIN
supra.SupraConf.ACCECC_CONTROL["credentials"] = "true"
supra.SupraConf.ACCECC_CONTROL["headers"] = "origin, content-type, accept"
supra.SupraConf.ACCECC_CONTROL["methods"] = "POST, GET, PUT, DELETE ,OPTIONS"


def check_login(function):
    @supra.access_control
    def check(request, *args, **kwargs):
        if request.user.is_authenticated() or request.method == "OPTIONS":
            paciente = Paciente.objects.filter(id=request.user.pk).first()
            if paciente:
                if paciente.activado:
                    return function(request, *args, **kwargs)
                # end if
            else:
                medico = Medico.objects.filter(id=request.user.pk).first()
                if medico:
                    if medico.activado:
                        return function(request, *args, **kwargs)
                    # end if
            return HttpResponse(simplejson.dumps({"error": "Debes activar tu cuenta"}), status=403)
            # end if
        return HttpResponse(simplejson.dumps({"error": "Debes iniciar sesion"}), status=403)
    # end def
    return check
# end def
