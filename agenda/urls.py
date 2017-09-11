from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^calendario/list/$', views.CalendarioCitaList.as_view(), name="calendarios"),
    url(r'^calendario/form/$', views.CalandarioCitaForm.as_view(), name="calendario_form"),
    url(r'^calendario/form/(?P<pk>\d+)/$', views.CalandarioCitaForm.as_view(), name="calendario_edit"),
    url(r'^calendario/delete/(?P<pk>\d+)/$', views.CalandarioCitaDelete.as_view(), name="calendario_delete"),
]
