from django.conf.urls import include, url
import views

"""
    Calendario
"""

urlpatterns = [
    url(r'^calendario/list/$', views.CalendarioCitaList.as_view(), name="calendarios"),
    url(r'^calendario/form/$', views.CalandarioCitaForm.as_view(), name="calendario_form"),
    url(r'^calendario/form/(?P<pk>\d+)/$', views.CalandarioCitaForm.as_view(), name="calendario_edit"),
    url(r'^calendario/delete/(?P<pk>\d+)/$', views.CalandarioCitaDelete.as_view(), name="calendario_delete"),
]

"""
    Citas medicas
"""

urlpatterns += [
    url(r'^cita/list/$', views.CitasMedicasList.as_view(), name="citas"),
    url(r'^cita/form/$', views.CitaMedicaForm.as_view(), name="cita_form"),
    url(r'^cita/form/(?P<pk>\d+)/$', views.CitaMedicaForm.as_view(), name="cita_edit"),
]


"""
    Procedimiento Medico
"""

urlpatterns += [
    url(r'^procedimiento/medico/list/$', views.ProcedimientosList.as_view(), name="procedimiento"),
]


"""
    Cancelar cita
"""
urlpatterns += [
    url(r'^cancelar/cita/form/(?P<pk>\d+)/$', views.CancelarCitaForm.as_view(), name="cancelar_cita"),
]
