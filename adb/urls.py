from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^movil/$', views.PublicidadMovilList.as_view(), name="publicidad_movil"),
]
