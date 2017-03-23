from django.conf.urls import url
from django.conf.urls import include

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    #url(r'^index2/$', views.index2, name='index2'),
    url(r'^patient/register$', views.PatientRegistration.register, name='patient_registration'),
	url(r'^patient/profile$', views.PatientProfile.view, name='patient_profile'),
    url(r'^patient/profile/update$', views.PatientProfile.update_basic, name='patient_profile_update'),
	url(r'^calendar/$', views.calendar, name='calendar'),
	url(r'^appt/', include('appointment.urls')),
    url(r'^admin/register_admin', views.Admin.register_admin, name='register_admin'),
    url(r'^admin/register_doctor', views.Admin.register_doctor, name='register_doctor'),
    url(r'^admin/register_nurse', views.Admin.register_nurse, name='register_nurse'),
    url(r'^nurse/select_doctor', views.Nurse.select_doctor, name='select_doctor'),
]