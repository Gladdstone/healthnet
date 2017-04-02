from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic import TemplateView

from .forms import *
from django.contrib.auth.models import User
from .models import *
from django.forms.formsets import formset_factory
from collections import OrderedDict
from calendar import HTMLCalendar
from datetime import *
from itertools import groupby
import random

from django.shortcuts import render_to_response
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.utils.html import conditional_escape as esc

def index(request):

    if request.user.is_authenticated() and request.user.first_name == 'patient':
        return render(
            request,
            'patient_home.html',
        )
    return render (
        request,
        'index.html',
    )

def index2(request):
    return render (
        request,
        'index2.html',
    )
	
def calendar(request):
    if request.method == "POST":
        return AppointmentCalendar.calendar(request, int(request.POST.get('year','')),int(request.POST.get('month','')))
    return AppointmentCalendar.calendar(request, datetime.now().year,datetime.now().month)

class PatientRegistration(generic.ListView):
    template_name = 'registration/dual_form.html'

    def register(request):
        if request.method == "POST":
            if "cancel" in request.POST:
                return redirect('index')
            form = RegisterUserForm(request.POST)
            form2 = RegisterPatientForm(request.POST)
            form3 = PatientMedicalInfoForm(request.POST)
            if all([form.is_valid(), form2.is_valid(), form3.is_valid()]) and not User.objects.filter(username=request.POST.get('username')).exists():
                userInfo = form.save(commit=False)
                userInfo.save()
                #User.objects.all().delete()

                user = User.objects.create_user(username = request.POST.get("username"), password = request.POST.get("password"), email = request.POST.get('email'), first_name = 'patient')

                profileInfo = form2.save(commit=False)
                medicalInfo = form3.save(commit=False)
                medicalInfo.save()
                profileInfo.user = user
                profileInfo.medical_info = medicalInfo
                profileInfo.save()
                medicalInfo.save()
                hospital = Hospital.objects.get(name=request.POST.get('pref_hospital'))
                hospital.people.add(user)
                hospital.save()
                try:
                    emergency_contact = User.objects.get(email=profileInfo.emergency_contact_email)
                    if emergency_contact != None and emergency_contact.patient_user_profile.first_name == profileInfo.emergency_contact_first_name and \
                                emergency_contact.patient_user_profile.last_name == profileInfo.emergency_contact_last_name: #checking if emergency contact info matches with patient in database
                        emergency_contact.patient_set.add(profileInfo)
                        profileInfo.save()
                        emergency_contact.save()
                    message = 'Emergency contact linked to existing patient'
                except Exception as err:
                    print("Exception {0}".format(err))
                    message = 'Emergency contact not linked to any existing patient'


                profileInfo.save()

                # log entry creation/save
                log_id = random.randrange(0, 99999)
                log_user = profileInfo.last_name
                log_message = "Patient registered"
                log = LogEntry(log_id, log_user, log_message)
                log.save()

                return render(request, 'return_home_message.html', {'message': message, 'url': 'index'})
        else:
            form = RegisterUserForm()
            form2 = RegisterPatientForm()
            form3 = PatientMedicalInfoForm()
        return render(request, 'tri_form.html', {'form': form, 'form2': form2, 'form3': form3, 'title': 'Register Patient'})

class PatientProfile(generic.edit.CreateView):

    def view(request):
        if request.method == "POST":

            if "update" in request.POST:
                return redirect('patient_profile_update')
            if "changePassword" in request.POST:
                return redirect('patient_change_password')
        else:
            profileInfo = request.user.patient_user_profile
            basicInfo = OrderedDict()
            basicInfo['First name'] = profileInfo.first_name
            basicInfo['Last name'] = profileInfo.last_name
            basicInfo['Phone number'] = profileInfo.phone_number
            basicInfo['Insurance'] = profileInfo.insurance
            basicInfo['Pref hospital'] = profileInfo.pref_hospital
            basicInfo['Emergency contact first name'] = profileInfo.emergency_contact_first_name
            basicInfo['Emergency contact last name'] = profileInfo.emergency_contact_last_name
            basicInfo['Emergency contact email'] = profileInfo.emergency_contact_email
        return render(request, 'patient_view_profile.html', {'basicInfo': basicInfo})

    def update_basic(request):
        if request.method == 'POST':
            if "cancel" in request.POST:
                return redirect('patient_profile')
            form = PatientUpdateBasicInfoForm(request.POST)
            if form.is_valid():
                form.save(commit=False)
                profileInfo = request.user.patient_user_profile
                for k, v in request.POST.items():
                    try:
                        setattr(profileInfo, k, v)
                    except:
                        pass
                profileInfo.save()
                try:
                    emergency_contact_old = profileInfo.emergency_contact
                    emergency_contact = User.objects.get(email=profileInfo.emergency_contact_email)
                    try:
                        emergency_contact_old.patient_set.remove(profileInfo)
                    except:
                        pass
                    if emergency_contact != None and emergency_contact.patient_user_profile.first_name == profileInfo.emergency_contact_first_name and \
                                emergency_contact.patient_user_profile.last_name == profileInfo.emergency_contact_last_name: #checking if emergency contact info matches with patient in database
                        emergency_contact.patient_set.add(profileInfo)
                        emergency_contact.save()
                        message = 'Emergency contact linked to existing patient'
                    else:
                        message = 'Emergency contact not linked to any existing patient'
                    profileInfo.save()
                except Exception as err:
                    print("Exception {0}".format(err))
                    message = 'Emergency contact not linked to any existing patient'

                    # log entry creation/save
                    log_id = random.randrange(0, 99999)
                    log_user = profileInfo.last_name
                    log_message = "Patient information updated"
                    log = LogEntry(log_id, log_user, log_message)
                    log.save()

                return render(request, 'return_home_message.html', {'message': message, 'url': 'index'})
               #patient.first_name = request.POST.get("first_name")
        else:
            patient = request.user.patient_user_profile
            form = PatientUpdateBasicInfoForm(instance = patient)
        return render(request, 'patient_update_profile.html', {'form': form})

    def update_password(request):
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                #update_session_auth_hash(request, user)  # uncomment if we want users to stay logged in after changing password
                message = 'Your password was successfully updated!'

                # log entry creation/save
                profileInfo = request.user.patient_user_profile
                log_id = random.randrange(0, 99999)
                log_user = profileInfo.last_name
                log_message = "Password changed"
                log = LogEntry(log_id, log_user, log_message)
                log.save()

                return render(request, 'return_home_message.html', {'message': message, 'url': 'index'})
            else:
                messages.error(request, 'Please correct the error below.')
        else:
            form = PasswordChangeForm(request.user)
        return render(request, 'change_password.html', {
            'form': form
        })

class AppointmentCalendar(HTMLCalendar):

    def __init__(self, appointments):
        super(AppointmentCalendar, self).__init__()
        self.appointments = self.group_by_day(appointments)

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' c_today'
            if day in self.appointments:
                cssclass += ' c_filled'
                body = ['<div class="c_dcontent"><ul>']
                for appointment in self.appointments[day]:
                    body.append('<li>')
                    #body.append('<a href="%s">' % appointment.get_absolute_url())
                    body.append(esc(appointment.time.strftime("%H:%M") + "-" + appointment.title))
                    body.append('</a></li>')
                body.append('</ul></div>')
                return self.day_cell(cssclass, '<div class="c_dnum">%d</div> %s' % (day, ''.join(body)))
            return self.day_cell(cssclass, day)
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(AppointmentCalendar, self).formatmonth(year, month)

    def group_by_day(self, appointments):
        field = lambda appointment: appointment.date.day
        return dict(
            [(day, list(items)) for day, items in groupby(appointments, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="c_day %s">%s</td>' % (cssclass, body)
	
    def formatmonthname(self, theyear, themonth, withyear=True):
        months = ['Placeholder','January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
        s = ('<form method="POST" class="post-form" id="m-post">'
		     'CSRF'
			 '<select name="month" onchange="this.form.submit();">'
             '<option value="1">'+months[1]+'</option><option value="2">'+months[2]+'</option><option value="3">'+months[3]+'</option>'
             '<option value="4">'+months[4]+'</option><option value="5">'+months[5]+'</option><option value="6">'+months[6]+'</option>'
             '<option value="7">'+months[7]+'</option><option value="8">'+months[8]+'</option><option value="9">'+months[9]+'</option>'
             '<option value="10">'+months[10]+'</option><option value="11">'+months[11]+'</option><option value="12">'+months[12]+'</option>'
             '</select>'
			 '<select name="year" onchange="this.form.submit();">'
             '<option>'+str(theyear-1)+'</option><option selected>'+str(theyear)+'</option><option>'+str(theyear+1)+'</option>'
             '</select>'
			 '</form>')
        
        m = months[themonth]
        #s = s.replace("<op>M",">C")
        s = s.replace("\">" + m, "\" selected>" + m)
        return '<tr><th colspan="7" class="month">%s</th></tr>' % s

    def calendar(request, year, month):	
        cal = AppointmentCalendar(request.user.patient_appointment.filter(month=month, year=year)).formatmonth(year, month)
        #cal = HTMLCalendar(firstweekday=0).formatmonth(year, month)
        return render(request, 'calendar.html', {'calendar': mark_safe(cal),})

def view_syslog(request):
    if request.user.is_superuser:
        profileInfo = request.user.patient_user_profile
        log_id = random.randrange(0, 99999)
        log_user = profileInfo.last_name
        log_message = "Password changed"
        log = LogEntry(log_id, log_user, log_message)
        log.save()
        return render(request, 'logfile')
    return redirect('index')




class Admin(generic.ListView):

    def register_admin(request):
        """
        An admin can register other admins
        :return: redirects to a template
        """
        if request.method == "POST":
            if "cancel" in request.POST:
                return redirect('index')
            form = RegisterUserForm(request.POST)
            form2 = RegisterAdminForm(request.POST);
            if all([form.is_valid(), form2.is_valid()]) and not User.objects.filter(username=request.POST.get('username')).exists():
                userInfo = form.save(commit=False)
                userInfo.save()
                user = User.objects.create_user(username = request.POST.get("username"), password = request.POST.get("password"), email = request.POST.get('email'), first_name = 'admin')
                profileInfo = form2.save(commit=False)
                profileInfo.user = user
                profileInfo.save()
                hospital = Hospital.objects.get(name=request.POST.get('hospital'))
                hospital.people.add(user)
                hospital.save()
                message = "Admin successfully added"

                # log entry creation/save
                profileInfo = request.user.patient_user_profile
                log_id = random.randrange(0, 99999)
                log_user = profileInfo.last_name
                log_message = "Administrator registered"
                log = LogEntry(log_id, log_user, log_message)
                log.save()

                return render(request, 'return_home_message.html', {'message': message, 'url': 'index'})
        else:
            form = RegisterUserForm()
            form2 = RegisterAdminForm()
        return render(request, '../templates/registration/dual_form.html', {'form': form, 'form2': form2, 'title': 'Register Admin'})

    def register_doctor(request):
        """
        An admin can register doctors
        :return: redirects to a template
        """
        if request.method == "POST":
            if "cancel" in request.POST:
                return redirect('index')
            form = RegisterUserForm(request.POST)
            form2 = RegisterDoctorForm(request.POST);
            if all([form.is_valid(), form2.is_valid()]) and not User.objects.filter(username=request.POST.get('username')).exists():
                userInfo = form.save(commit=False)
                userInfo.save()
                user = User.objects.create_user(username = request.POST.get("username"), password = request.POST.get("password"), email = request.POST.get('email'), first_name = 'doctor')
                profileInfo = form2.save(commit=False)
                profileInfo.user = user
                profileInfo.save()
                hospital = Hospital.objects.get(name=request.POST.get('hospital'))
                hospital.people.add(user)
                hospital.save()
                message = "Doctor successfully added"

                # log entry creation/save
                profileInfo = request.user.patient_user_profile
                log_id = random.randrange(0, 99999)
                log_user = profileInfo.last_name
                log_message = "Doctor registered"
                log = LogEntry(log_id, log_user, log_message)
                log.save()

                return render(request, 'return_home_message.html', {'message': message, 'url': 'index'})
        else:
            form = RegisterUserForm()
            form2 = RegisterDoctorForm()
        return render(request, '../templates/registration/dual_form.html', {'form': form, 'form2': form2, 'title': 'Register Doctor'})

    def register_nurse(request):
        """
        An admin can register nurses
        :return: redirects to a template
        """
        if request.method == "POST":
            if "cancel" in request.POST:
                return redirect('index')
            form = RegisterUserForm(request.POST)
            form2 = RegisterNurseForm(request.POST);
            if all([form.is_valid(), form2.is_valid()]) and not User.objects.filter(username=request.POST.get('username')).exists():
                userInfo = form.save(commit=False)
                userInfo.save()
                user = User.objects.create_user(username = request.POST.get("username"), password = request.POST.get("password"), email = request.POST.get('email'), first_name = 'nurse')
                profileInfo = form2.save(commit=False)
                profileInfo.user = user
                profileInfo.save()
                hospital = Hospital.objects.get(name=request.POST.get('hospital'))
                hospital.people.add(user)
                hospital.save()
                message = "Nurse successfully added"

                # log entry creation/save
                profileInfo = request.user.patient_user_profile
                log_id = random.randrange(0, 99999)
                log_user = profileInfo.last_name
                log_message = "Nurse registered"
                log = LogEntry(log_id, log_user, log_message)
                log.save()

                return render(request, 'return_home_message.html', {'message': message, 'url': 'index'})
        else:
            form = RegisterUserForm()
            form2 = RegisterNurseForm()
        return render(request, '../templates/registration/dual_form.html', {'form': form, 'form2': form2, 'title': 'Register Nurse'})

    def register_hospital(request):
        if request.method == 'POST':
            if "cancel" in request.POST:
                return redirect('index')
            form = AddHospitalForm(request.POST)
            if form.is_valid():
                form.save()
                message = "Hospital successfully added"
                return render(request, 'return_home_message.html', {'message': message, 'url': 'index'})
        else:
            form = AddHospitalForm()
        return render(request, 'form_generic.html', {'form': form, 'title': 'Register Hospital'})

    def transfer_patient(request):
        if request.method == 'POST':
            if 'cancel' in request.POST:
                return redirect('index')
            form = TransferPatientForm(request.POST)
            if form.is_valid():
                #form.save()
                patient = User.objects.get(username=request.POST.get('patient'))
                profileInfo = patient.patient_user_profile
                hospital = Hospital.objects.get(name=request.POST.get('hospital'))
                hospital.people.add(patient)
                profileInfo.current_hospital = hospital
                profileInfo.save()
                message = 'Patient: {} {} transferred to Hospital: {}'.format(profileInfo.first_name, profileInfo.last_name, hospital)
                return render(request, 'return_home_message.html', {'message': message, 'url': 'index'})
        else:
            form = TransferPatientForm()
        return render(request, 'form_generic.html', {'form': form, 'title': 'Transfer Patient'})

class Nurse(generic.ListView):

    def select_doctor(request):
        """
        Display a list of doctors in the hospital that the nurse works in
        Allow the nurse to choose a specific doctor and the nurse's value for current doctor will be updated
        :return: redirects to a template
        """
        if request.method == 'POST':
            form = SelectDoctorForm(request.POST, hospital=request.user.hospital_set.all()) # *** HOSPITAL SHOULD BE THE HOSPITAL THE NURSE WORKS IN, ONCE HOSPITAL IS IMPLEMENTED ***
            if "cancel" in request.POST:
                return redirect('index')
            if form.is_valid():
                doctor = User.objects.get(username=request.POST.get('doctors'))
                request.method = 'GET'
                profileInfo = request.user.nurse_user_profile
                profileInfo.current_doctor = doctor
                profileInfo.save()
                message = 'Current doctor is now: {} {}'.format(doctor.doctor_user_profile.first_name, doctor.doctor_user_profile.last_name)

                # log entry creation/save
                profileInfo = request.user.patient_user_profile
                log_id = random.randrange(0, 99999)
                log_user = profileInfo.last_name
                log_message = "Doctor selected"
                log = LogEntry(log_id, log_user, log_message)
                log.save()

                return render(request, 'return_home_message.html', {'message': message, 'url': 'index'})
        else:
            form = SelectDoctorForm(hospital=request.user.hospital_set.all())
        return render(request, 'form_generic.html', {'form': form, 'title': 'Select Doctor'})




class Doctor(generic.ListView):
    pass



class PrivateMessage(generic.ListView):
    def view_messages(request):
        """

        :return:
        """
        if request.method == 'POST':
            if ('create' in request.POST):
                return redirect('create_message', None)
            form = ViewMessagesForm(request.POST, user=request.user)
            if form.is_valid():
                messages = request.user.receiver.all()
                message = messages.get(identifier=request.POST.get('message'))
                return redirect('read_message', message)
        else:
            form = ViewMessagesForm(user=request.user)
        return render(request, 'view_messages.html', {'form': form, 'title': 'View Messages'})


    def create_message(request, receiver):
        if request.method == 'POST':
            if ('cancel' in request.POST):
                return redirect('view_messages')
            form = CreateMessageForm(request.POST, user=request.user, receiver=receiver)
            if (form.is_valid()):
                post = form.save(commit=False)
                post.sender = request.user
                post.receiver = User.objects.get(username=request.POST.get('receiver_field'))
                post.created_at = datetime.now().strftime('%H:%M:%S')
                post.save()
                message = 'Private message sent'
                return render(request, 'return_home_message.html', {'message': message, 'url': 'index'})
        else:
            form = CreateMessageForm(user=request.user, receiver=receiver)
        return render(request, 'form_generic.html', {'form': form, 'title': 'Create Message'})


    def read_message(request, message):
        if request.method == 'POST':
            if ('back' in request.POST):
                return redirect('view_messages')
            form = ReadMessageForm(request.POST)
            if('reply' in request.POST):
                receiver = request.POST.get('sender_field')
                return redirect('create_message', receiver)
        form = ReadMessageForm(instance=request.user.receiver.get(identifier = message))
        return render(request, 'read_message.html', {'form': form, 'title': 'Read Message'})

class GenericUser(generic.ListView):
    def select_patient(request):
        if request.method == 'POST':
            form = SelectPatientForm(request.POST, hospital=request.user.hospital_set.all()) # *** HOSPITAL SHOULD BE THE HOSPITAL THE NURSE WORKS IN, ONCE HOSPITAL IS IMPLEMENTED ***
            if "cancel" in request.POST:
                return redirect('index')
            if form.is_valid():
                patient = request.POST.get('patient')
                return redirect('edit_medical_info', patient)
        else:
            form = SelectPatientForm(hospital=request.user.hospital_set.all())
        return render(request, 'select_form.html', {'form': form, 'title': 'Select Patient'})

    def edit_medical_info(request, patient):
        if request.method == 'POST':
            form = EditMedicalInfoForm(request.POST) # *** HOSPITAL SHOULD BE THE HOSPITAL THE NURSE WORKS IN, ONCE HOSPITAL IS IMPLEMENTED ***
            if "cancel" in request.POST:
                return redirect('index')
            if form.is_valid():
                medicalInfo = form.save(commit=False)
                patientProfile = User.objects.get(username=patient).patient_user_profile
                medicalInfo.save()
                patientProfile.medical_info = medicalInfo
                patientProfile.save()
                message = 'Patient medical info updated'
                return render(request, 'return_home_message.html', {'message': message, 'url': 'index'})
        else:
            patientProfile = User.objects.get(username=patient).patient_user_profile
            form = EditMedicalInfoForm(instance=patientProfile.medical_info)
        return render(request, 'form_generic.html', {'form': form, 'title': 'Update {} {}\'s Medical Info'.format(patientProfile.first_name, patientProfile.last_name)})

    def admit_patient(request):
        if request.method == 'POST':
            if 'cancel' in request.POST:
                return redirect('index')
            form = AdmitPatientForm(request.POST, user=request.user)
            if form.is_valid():
                #form.save(commit=False)
                patient = User.objects.get(username=request.POST.get('patient'))
                profileInfo = patient.patient_user_profile
                hospital = Hospital.objects.get(name=request.POST.get('hospital'))
                hospital.people.add(patient)
                profileInfo.current_hospital = hospital
                profileInfo.save()
                message = 'Patient: {} {} admitted to Hospital: {}'.format(profileInfo.first_name, profileInfo.last_name, hospital)
                return render(request, 'return_home_message.html', {'message': message, 'url': 'index'})
        else:
            form = AdmitPatientForm(user=request.user)
        return render(request, 'form_generic.html', {'form': form, 'title': 'Admit Patient'})