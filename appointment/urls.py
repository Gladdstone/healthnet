from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.Home.index, name='home'),
    url(r'^view/', views.Appointment.view, name='appointments'),
    url(r'^create/', views.Appointment.create, name='create_appointment'),
    url(r'^update/(?P<title>.+?)/(?P<username>.+?)/$', views.Appointment.update, name='update_appointment'),
]
