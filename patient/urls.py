from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.Home.index, name='home'),
    url(r'^register/', views.PatientRegistration.register, name='patient_registration'),
]