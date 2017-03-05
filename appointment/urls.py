from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.Home.index, name='home'),
    url(r'^view/', views.appointments, name='appointments'),
    url(r'^create/', views.CreateAppointment.create, name='create_appointment')
]
