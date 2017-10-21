from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^confirmacion/$', views.confirmacion , name="confirmacion"),
    url(r'^nueva/confirmacion/$', views.generarConfirmacion , name="nueva_confirmacion"),
    url(r'^paciente/form/$', views.PacienteSupraForm.as_view(), name="paciente_form"),
    url(r'^paciente/form/(?P<pk>\d+)/$', views.PacienteSupraForm.as_view(), name="paciente_form_edit"),
    url(r'^login/$', views.LoginU.as_view(), name="loginU"),
    url(r'^logout/$', views.logoutUser, name="loginU"),
    url(r'^chhange/password/$', views.change_password, name="change_password"),
    url(r'^is/login/$', views.islogin, name="islogin"),
]
