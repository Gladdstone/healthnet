from django.conf.urls import url
from django.conf.urls import include

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    #url(r'^index2/$', views.index2, name='index2'),
    url(r'^patient/register$', views.PatientRegistration.register, name='patient_registration'),
	url(r'^patient/profile$', views.PatientProfile.view, name='patient_profile'),
    url(r'^patient/profile/update$', views.PatientProfile.update_basic, name='patient_profile_update'),
    url(r'^patient/profile/changepassword$', views.PatientProfile.update_password, name='patient_change_password'),
    url(r'^prescriptions/view/(?P<patient>.+?)/$', views.Prescription.view_prescriptions, name='view_prescriptions'),
    url(r'^prescriptions/create/(?P<patient>.+?)/$', views.Prescription.create_prescriptions, name='create_prescriptions'),
    url(r'^calendar/$', views.calendar, name='calendar'),
	url(r'^appt/', include('appointment.urls')),
    url(r'^admin/register_admin', views.Admin.register_admin, name='register_admin'),
    url(r'^admin/register_doctor', views.Admin.register_doctor, name='register_doctor'),
    url(r'^admin/register_nurse', views.Admin.register_nurse, name='register_nurse'),
    url(r'^admin/register_hospital', views.Admin.register_hospital, name='register_hospital'),
    url(r'^admin/transfer_patient', views.Admin.transfer_patient, name='transfer_patient'),
    url(r'^nurse/select_doctor', views.Nurse.select_doctor, name='select_doctor'),
    url(r'^doctor/discharge_patient', views.Doctor.discharge_patient, name='discharge_patient'),
    url(r'^select_patient/(?P<redirectUrl>.+?)/$', views.GenericUser.select_patient, name='select_patient'),
    url(r'^edit_medical_info/(?P<patient>.+?)/$', views.GenericUser.edit_medical_info, name='edit_medical_info'),
    url(r'^admit_patient', views.GenericUser.admit_patient, name='admit_patient'),
    url(r'^message/view', views.PrivateMessage.view_messages, name='view_messages'),
    url(r'^message/create/(?P<receiver>.+?)/$', views.PrivateMessage.create_message, name='create_message'),
    url(r'^message/create/$', views.PrivateMessage.create_message, name='create_message'),
    url(r'^message/read/(?P<message>.+?)/$', views.PrivateMessage.read_message, name='read_message'),
    url(r'^test/read/(?P<test>.+?)/$', views.Tests.read_test, name='read_test'),
    url(r'^test/view/(?P<patient>.+?)/$', views.Tests.view_tests, name='view_tests'),
    url(r'^test/edit/(?P<patient>.+?)/(?P<test>.+?)/$', views.Tests.edit_test, name='edit_test'),
    url(r'^admin/log$', views.Log.view_log, name='view_log'),
    url(r'^admin/statistics$', views.SystemStatistics.view_statistics, name='view_statistics'),

]