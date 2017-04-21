from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^view/', views.Appointment.view, name='appointments'),
    url(r'^create/', views.Appointment.create, name='create_appointment'),
    url(r'^update/(?P<id>.+?)/(?P<username>.+?)/$', views.Appointment.update, name='update_appointment'),
]
