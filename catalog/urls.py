from django.conf.urls import url
from django.conf.urls import include

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    #url(r'^index2/$', views.index2, name='index2'),
    url(r'^patient/register/', views.PatientRegistration.register, name='patient_registration'),
	url(r'^patient/profile/', views.PatientProfile.view, name='patient_profile'),
    url(r'^patient/profile/update', views.PatientProfile.update_basic, name='patient_profile_update'),
	url(r'^appt/', include('appointment.urls')),
]