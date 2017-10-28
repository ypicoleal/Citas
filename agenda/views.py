# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from supra import views as supra
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from Citas.decorator import check_login
from django.views.decorators.csrf import csrf_exempt
from usuarios.models import Paciente
from Citas.settings import APIKEY, ORIGIN
import models, json, forms, md5, random
supra.SupraConf.body = True
# Create your views here.
supra.SupraConf.ACCECC_CONTROL["allow"] = True
supra.SupraConf.ACCECC_CONTROL["origin"] = ORIGIN
supra.SupraConf.ACCECC_CONTROL["credentials"] = "true"
supra.SupraConf.ACCECC_CONTROL["headers"] = "origin, content-type, accept"
supra.SupraConf.ACCECC_CONTROL["methods"] = "POST, GET, PUT, DELETE ,OPTIONS"


"""
    CalendarioCita
"""
class CalendarioCitaList(supra.SupraListView):
    model = models.CalendarioCita
    list_display = ['id', 'title', 'start', 'end', 'color', 'almuerzo', 'asignacionCita', 'name']
    list_filter = ['inicio__year', 'inicio__month', 'inicio__day', 'almuerzo']

    def start(self, obj, row):
        return obj.inicio.strftime('%Y-%m-%d %H:%M:%S')

    def end(self, obj, row):
        return obj.fin.strftime('%Y-%m-%d %H:%M:%S')

    def name(self, obj, row):
        return u"%s %s" % (obj.inicio.strftime('%H:%M:%S'), obj.fin.strftime('%H:%M:%S'))

    def asignacionCita(self, obj, row):
        asignacion = models.CitaMedica.objects.filter(calendario=obj).first()
        if asignacion:
            nombre = "%s %s" % (asignacion.paciente.first_name, asignacion.paciente.last_name)
            return {"id": asignacion.id, "nombre": nombre}
        return None

    def title(self, obj, row):
        title = "Espacio para cita"
        if obj.almuerzo:
            title = "Almuerzo"
        asignacion = self.asignacionCita(obj, row)
        if asignacion:
            title = "Cita: %s" % asignacion["nombre"]
        return title

    def color(self, obj, row):
        color = "#2196f3"
        if obj.almuerzo:
            color = "#f44336"
        elif self.asignacionCita(obj, row):
            color = "#9c27b0"
        return color

    @method_decorator(check_login)
    def dispatch(self, request, *args, **kwargs):
        return super(CalendarioCitaList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        filtro = self.request.GET.get('citamedica', False)
        queryset = super(CalendarioCitaList, self).get_queryset()
        if filtro:
            queryset = queryset.filter(citamedica=None)
        return queryset.filter(eliminado=False)
    # end def
# end class


class CalandarioCitaForm(supra.SupraFormView):
    model = models.CalendarioCita
    form_class = forms.CalendarioCitaForm

    def get_form_class(self):
        if 'pk' in self.http_kwargs:
            self.form_class = forms.CalendarioCitaFormEdit
        # end if
        return self.form_class
    # end class

    @method_decorator(check_login)
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(CalandarioCitaForm, self).dispatch(request, *args, **kwargs)


class CalandarioCitaDelete(supra.SupraDeleteView):
    model = models.CalendarioCita

    @method_decorator(check_login)
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(CalandarioCitaDelete, self).dispatch(request, *args, **kwargs)
    # end def

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        asignacion = models.CitaMedica.objects.filter(calendario=self.object).first()
        if not asignacion:
            self.object.eliminado = True
            self.object.save()
            return HttpResponse({"exito": "eliminado"},status=200, content_type="application/json")
        else:
            return HttpResponse({"error": "No se puede borrar porque existe una cita agenda para esta fecha"}, status=400, contentType="application/json")
    # end def
# end class

"""
    CitaMedica
"""


class CitasMedicasList(supra.SupraListView):
    model = models.CitaMedica
    list_display = ['id', 'paciente', 'procedimiento', 'procedimiento__nombre', 'procedimiento__modalidad', 'entidad', 'entidad_nombre', 'estado', 'confirmacion', 'cancelar', 'fecha', 'inicio', 'fin', 'reprogramar', 'estado_nombre']
    list_filter = ['paciente', 'procedimiento', 'entidad', 'estado', 'confirmacion', 'calendario__inicio__year', 'calendario__inicio__month', 'calendario__inicio__day', 'calendario__inicio__range']

    @method_decorator(check_login)
    def dispatch(self, request, *args, **kwargs):
        return super(CitasMedicasList, self).dispatch(request, *args, **kwargs)

    def entidad_nombre(self, obj, row):
        if obj.entidad == 1:
            return "Particular"
        elif obj.entidad == 2:
            return "Medisanitas"
        # end if
        return "Colsanitas"
    # end def

    def estado_nombre(self, obj, row):
        if obj.estado == 1:
            return "Vigente"
        elif obj.estado == 2:
            return "Cancelado"
        # end if
        return "Vencida"
    # end def

    def confirmacion(self, obj, row):
        if obj.confirmacion == 1:
            return "Confirmado"
        # end if
        return "Cancelado"
    # end def

    def fecha(self, obj, row):
        if obj.calendario:
            return "%s" % (obj.calendario.inicio.strftime('%Y-%m-%d'))
        # end
        return None
    # end

    def inicio(self, obj, row):
        if obj.calendario:
            return obj.calendario.inicio.strftime('%H:%M:%S')
        # end if
        return None
    # end def

    def fin(self, obj, row):
        if obj.calendario:
            return obj.calendario.fin.strftime('%H:%M:%S')
        # end if
        return None
    # end def

    def reprogramar(self, obj, row):
        return models.CitaReprogramada.objects.filter(cita=obj.id).count()
    # end def

    def get_queryset(self):
        queryset = super(CitasMedicasList, self).get_queryset()
        paciente = Paciente.objects.filter(id=self.request.user.pk).first()
        if paciente:
            queryset = queryset.filter(paciente=paciente.id)
        return queryset.filter(eliminado=False)
    # end def
# end class

class CitaMedicaForm(supra.SupraFormView):
    model = models.CitaMedica
    form_class = forms.CitaMedicaFormSupra

    @method_decorator(check_login)
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(CitaMedicaForm, self).dispatch(request, *args, **kwargs)

# end class

"""
    Procedimientos
"""

class ProcedimientosList(supra.SupraListView):
    model = models.ProcedimientoMedico
    list_display = ['nombre', 'precio', 'modalidad', 'id']
    search_fields = ['nombre', 'precio']
    list_filter = ['modalidad', ]

    def get_queryset(self):
        queryset = super(ProcedimientosList, self).get_queryset()
        return queryset.filter(eliminado=False)
    # end def

    @method_decorator(check_login)
    def dispatch(self, request, *args, **kwargs):
        return super(ProcedimientosList, self).dispatch(request, *args, **kwargs)
# end class


"""
    Cancelar cita
"""

class CancelarCitaForm(supra.SupraFormView):
    model = models.CitaMedica
    form_class = forms.CancelarCitaForm

    @method_decorator(check_login)
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(CancelarCitaForm, self).dispatch(request, *args, **kwargs)
# end class


"""
    Reprogramar cita
"""

class ReprogramarCitaSupra(supra.SupraFormView):
    model = models.CitaReprogramada
    form_class = forms.ReprogramarCitaFormSupra

    @method_decorator(check_login)
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(ReprogramarCitaSupra, self).dispatch(request, *args, **kwargs)
# end class


"""
    Minutos restantes
"""

class MinutosRestanteSupra(supra.SupraFormView):
    model = models.DuracionCita

    @method_decorator(check_login)
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(MinutosRestanteSupra, self).dispatch(request, *args, **kwargs)
# end class


def minutosRestanteCita(request, pk):
    minutos = models.DuracionCita.objects.filter(cita__id=pk).last()
    if minutos:
        restante = minutos.duracion_r
    else:
        restante = 0
    # end if
    return HttpResponse(json.dumps({"minutos": restante}), status=200, content_type="application/json")
# end def

def pagar(request, pk):
    currency = request.GET.get('currency', 'COP')
    cita = models.CitaMedica.objects.filter(id=pk).first()
    if cita:
        merchantId = 673242
        accountId = 675923
        referenceCode = "%s%s00%d%d" % (random.choice(cita.paciente.first_name), random.choice(cita.paciente.last_name), cita.procedimiento.id, cita.id)
        description = cita.procedimiento.nombre
        buyerEmail = cita.paciente.email
        buyerFullName = "%s %s" % (cita.paciente.first_name, cita.paciente.last_name)
        if currency == "USD":
            amount = cita.procedimiento.precio_usd
        else:
            amount = cita.procedimiento.precio
        signature = "%s~%d~%s~%d~%s" % (APIKEY, merchantId, referenceCode, amount, currency)
        signatureMD5 = md5.new(signature)
        confirmationUrl = "http://app.dranilsaarias.com/agenda/confirmacion/%d/pago/" % (cita.id)
        return render(request, 'agenda/compra.html', {"merchantId": merchantId, "accountId":accountId, "referenceCode":referenceCode ,"buyerFullName":buyerFullName, "description": description, "currency": currency, "amount": amount, "buyerEmail": buyerEmail, "signature":signatureMD5.hexdigest(), "confirmationUrl": confirmationUrl})
    # end if
    # end if
    return HttpResponseNotFound('<h1>Pagina no encontrada.</h1>')
# end def

def new_value(value):
    val = value.split(".")
    try:
        if val[1] == "00":
            num = val[0]+".0"
        else:
            num = value
        return num
    except:
        return value
# end if

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@supra.access_control
@csrf_exempt
def confirmacion(request, pk):
    if request.method == "POST":
        file = open(os.path.join(BASE_DIR, "confirmacion.txt"), "w+")
        file.write(str(request.POST))
        file.close()
        cita = models.CitaMedica.objects.filter(id=pk).first()
        form = forms.ConfirmacionPago(request.POST)
        if form.is_valid():
            con = form.save(commit=False)
            value = new_value(con.value)
            validacion = "%s~%d-%s~%s~%s~%s" % (APIKEY, con.merchantId, con.reference_sale, value, con.currency, con.state_pol)
            validacionMD5 = md5.new(validacion)
            if sign == validacionMD5:
                con.validacion = True
            else:
                con.validacion = False
            # end if
            if con.state_pol == '4':
                cita.pago = True
                cita.save()
            # end if
            con.cita = cita
            con.save()
            return HttpResponse(status=200)
        # end if
    return HttpResponse(status=400)
# end def
