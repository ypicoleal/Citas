from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^confirmacion/$', views.confirmacion , name="confirmacion"),
    url(r'^nueva/confirmacion/$', views.generarConfirmacion , name="nueva_confirmacion"),
]
