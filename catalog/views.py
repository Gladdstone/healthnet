from django.http import Http404
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

from django.shortcuts import render_to_response
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
import random
from django.utils import timezone

from django.utils.html import conditional_escape as esc



def index(request):

    if request.user.is_authenticated() and request.user.first_name == 'patient':
        return render(
            request,
            'index.html'
        )
    return render (
        request,
        'index.html'
    )
	
def calendar(request):
    if (not request.user.is_authenticated()):
        raise Http404
    if request.method == "POST":
        return AppointmentCalendar.calendar(request, int(request.POST.get('year','')),int(request.POST.get('month','')))
    return AppointmentCalendar.calendar(request, datetime.now().year,datetime.now().month)

class PatientRegistration(generic.ListView):

    def register(request):
        """
        View to register a patient
        :return: redirects to a template or another view
        """
        if request.user.is_authenticated():
            raise Http404
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
                log_user = None
                log_message = "Patient registered"
                log = LogEntry( user= log_user, message=log_message, time = timezone.now())
                log.save()
                stats = SysStats.objects.get(hospital=hospital)

                if(stats.patient_count == 0):
                    stats.patient_count = 1
                else:
                    stats.patient_count = stats.patient_count + 1

                stats.save()


                return render(request, 'return_home_message.html', {'message': message, 'url': 'index'})
        else:
            form = RegisterUserForm()
            form2 = RegisterPatientForm()
            form3 = PatientMedicalInfoForm()
        return render(request, 'tri_form.html', {'form': form, 'form2': form2, 'form3': form3, 'title': 'Register Patient'})

class PatientProfile(generic.edit.CreateView):

    def view(request):
        """
        View for a patient to view his profile
        :return: redirects to a template or another view
        """
        if (not request.user.is_authenticated()) or request.user.first_name != 'patient':
            raise Http404
        if request.method == "POST":
            if "update" in request.POST:
                return redirect('patient_profile_update')
            if "changePassword" in request.POST:
                return redirect('patient_change_password')
            if "prescriptions" in request.POST:
                return redirect('view_prescriptions', None)
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

            # log entry creation/save
            #log_id = random.randrange(0, 99999)
            log_user = request.user
            log_message = "Patient profile viewed"
            log = LogEntry(user=log_user, message=log_message, time=datetime.now())
            log.save()

        return render(request, 'patient_view_profile.html', {'basicInfo': basicInfo})

    def update_basic(request):
        """
        View for a patient to update his basic information
        :return: redirects to a template or another view
        """
        if (not request.user.is_authenticated()) or request.user.first_name != 'patient':
            raise Http404
        if request.method == 'POST': #submitting form
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
                    log_user = profileInfo.last_name
                    log_message = "Patient information updated"
                    log = LogEntry(user=log_user, message=log_message, time=timezone.now())
                    log.save()
                return render(request, 'return_home_message.html', {'message': message, 'url': 'index'})
               #patient.first_name = request.POST.get("first_name")
        else:#loading page
            patient = request.user.patient_user_profile
            form = PatientUpdateBasicInfoForm(instance = patient)
        return render(request, 'patient_update_profile.html', {'form': form})


    def update_password(request):
        """
        View for a patient to change his password
        :return: redirects to a template or another view
        """
        if (not request.user.is_authenticated()) or request.user.first_name != 'patient':
            raise Http404
        if request.method == 'POST':
            if "cancel" in request.POST:
                return redirect('patient_profile')
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                #update_session_auth_hash(request, user)  # uncomment if we want users to stay logged in after changing password
                message = 'Your password was successfully updated!'
                profileInfo = request.user.patient_user_profile

                # log entry creation/save
                log_user = profileInfo.last_name
                log_message = "Password updated"
                log = LogEntry(user=log_user, message=log_message, time=timezone.now())
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

    def __init__(self, appointments, nurse):
        super(AppointmentCalendar, self).__init__()
        self.appointments = self.group_by_day(appointments)
        self.nurse = nurse

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' c_today'
            if day in self.appointments and (self.nurse == 0 or date.today() + timedelta(-7) <= date(self.year, self.month, day) <= date.today() + timedelta(7)):
                cssclass += ' c_filled'
                body = ['<div class="c_dcontent"><ul>']
                for appointment in self.appointments[day]:
                    body.append('<li>')
                    #body.append('<a href="{% url \'patient_profile\'  %}"> ')
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
			 '<select class="c_select" name="month" onchange="this.form.submit();">'
             '<option value="1">'+months[1]+'</option><option value="2">'+months[2]+'</option><option value="3">'+months[3]+'</option>'
             '<option value="4">'+months[4]+'</option><option value="5">'+months[5]+'</option><option value="6">'+months[6]+'</option>'
             '<option value="7">'+months[7]+'</option><option value="8">'+months[8]+'</option><option value="9">'+months[9]+'</option>'
             '<option value="10">'+months[10]+'</option><option value="11">'+months[11]+'</option><option value="12">'+months[12]+'</option>'
             '</select>'
			 '<select class="c_select" name="year" onchange="this.form.submit();">'
             '<option>'+str(theyear-1)+'</option><option selected>'+str(theyear)+'</option><option>'+str(theyear+1)+'</option>'
             '</select>'
			 '</form>')
        
        m = months[themonth]
        #s = s.replace("<op>M",">C")
        s = s.replace("\">" + m, "\" selected>" + m)
        return '<tr><th colspan="7" class="month">%s</th></tr>' % s

    def calendar(request, year, month):
        if (not request.user.is_authenticated()):
            raise Http404
        if(request.user.first_name == 'nurse'):
            user = request.user.nurse_user_profile.current_doctor
            if user == None:
                return redirect('select_doctor')
        else:
            user = request.user
        if(user.first_name == 'doctor'):
            appointment_list = user.doctor_appointment
        else:
            appointment_list = user.patient_appointment

        if (request.user.first_name == 'nurse'):
            cal = AppointmentCalendar(appointment_list.filter(month=month, year=year), 1).formatmonth(year, month)
        else:
            cal = AppointmentCalendar(appointment_list.filter(month=month, year=year), 0).formatmonth(year, month)
        #cal = HTMLCalendar(firstweekday=0).formatmonth(year, month)
        return render(request, 'calendar.html', {'calendar': mark_safe(cal),})

def view_syslog(request):
    if request.user.is_superuser:

        # log entry creation/save
        log_user = request.user
        log_message = "System log viewed"
        log = LogEntry(user=log_user, message=log_message, time=timezone.now())
        log.save()
        return render(request, 'logfile')
    return redirect('index')




class Admin(generic.ListView):

    def register_admin(request):
        """
        View for an admin to register an admin
        :return: redirects to a template or another view
        """
        if (not request.user.is_authenticated()) or request.user.first_name != 'admin':
            raise Http404
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
                log_user = request.user
                log_message = "Admin registered"
                log = LogEntry(user=log_user, message=log_message, time=timezone.now())
                log.save()

                stats = SysStats.objects.get(hospital=hospital)
                if(stats.admin_count == 0):
                    stats.admin_count = 1
                else:
                    stats.admin_count += 1

                stats.save()


                return render(request, 'return_home_message.html', {'message': message, 'url': 'index'})
        else:
            form = RegisterUserForm()
            form2 = RegisterAdminForm()
        return render(request, '../templates/registration/dual_form.html', {'form': form, 'form2': form2, 'title': 'Register Admin'})

    def register_doctor(request):
        """
        View for an admin to register a doctor
        :return: redirects to a template or another view
        """
        if (not request.user.is_authenticated()) or request.user.first_name != 'admin':
            raise Http404
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
                log_user = request.user
                log_message = "Doctor registered"
                log = LogEntry(user=log_user, message=log_message, time=timezone.now())
                log.save()

                stats = SysStats.objects.get(hospital=hospital)
                if(stats.doctor_count == 0):
                    stats.doctor_count = 1
                else:
                    stats.doctor_count += 1
                stats.save()

                return render(request, 'return_home_message.html', {'message': message, 'url': 'index'})
        else:
            form = RegisterUserForm()
            form2 = RegisterDoctorForm()
        return render(request, '../templates/registration/dual_form.html', {'form': form, 'form2': form2, 'title': 'Register Doctor'})

    def register_nurse(request):
        """
        View for an admin to register a nurse
        :return: redirects to a template or another view
        """
        if (not request.user.is_authenticated()) or request.user.first_name != 'admin':
            raise Http404
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
                log_user = request.user
                log_message = "Nurse registered"
                log = LogEntry(user=log_user, message=log_message, time=timezone.now())
                log.save()

                stats = SysStats.objects.get(hospital=hospital)
                if(stats.nurse_count == 0):
                    stats.nurse_count = 1
                else:
                    stats.nurse_count += 1
                stats.save()

                return render(request, 'return_home_message.html', {'message': message, 'url': 'index'})
        else:
            form = RegisterUserForm()
            form2 = RegisterNurseForm()
        return render(request, '../templates/registration/dual_form.html', {'form': form, 'form2': form2, 'title': 'Register Nurse'})

    def register_hospital(request):
        """
        View for an admin to register a hospital
        :return: redirects to a template or another view
        """
        if (not request.user.is_authenticated()) or request.user.first_name != 'admin':
            raise Http404
        if request.method == 'POST':
            if "cancel" in request.POST:
                return redirect('index')
            form = AddHospitalForm(request.POST)
            if form.is_valid():
                hospital = form.save(commit=False)
                message = "Hospital successfully added"

                # log entry creation/save
                log_user = request.user
                log_message = "Hospital registered"
                log = LogEntry(user=log_user, message=log_message, time=timezone.now())
                log.save()
                hospital.save()
                stats = SysStats()
                stats.hospital = hospital

                stats.save()
                print(SysStats.objects.all())
                stats2 = SysStats.objects.get(hospital=hospital)


                return render(request, 'return_home_message.html', {'message': message, 'url': 'index'})
        else:
            form = AddHospitalForm()
        return render(request, 'form_generic.html', {'form': form, 'title': 'Register Hospital'})

    def transfer_patient(request):
        """
        View for an admin to transfer a patient from one hospital to another
        :return: redirects to a template or another view
        """
        if (not request.user.is_authenticated()) or request.user.first_name != 'admin':
            raise Http404
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

                prev_hospital = profileInfo.current_hospital
                if prev_hospital != None:
                    stats = SysStats.objects.get(hospital=prev_hospital)
                    admissionInfo = AdmissionInfo()
                    admissionInfo.patient = patient
                    admissionInfo.admission_time = profileInfo.admission_time
                    admissionInfo.discharge_time = timezone.now()
                    admissionInfo.statistics = stats
                    admissionInfo.save()
                    stats.save()

                profileInfo.admission_time = timezone.now()
                profileInfo.current_hospital = hospital
                profileInfo.save()
                message = 'Patient: {} {} transferred to Hospital: {}'.format(profileInfo.first_name, profileInfo.last_name, hospital)

                # log entry creation/save
                log_user = request.user
                log_message = "Patient transferred"
                log = LogEntry(user=log_user, message=log_message, time=timezone.now())
                log.save()



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
        if (not request.user.is_authenticated()) or request.user.first_name != 'nurse':
            raise Http404
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
                return render(request, 'return_home_message.html', {'message': message, 'url': 'index'})
        else:
            form = SelectDoctorForm(hospital=request.user.hospital_set.all())
        return render(request, 'form_generic.html', {'form': form, 'title': 'Select Doctor'})




class Doctor(generic.ListView):
    def discharge_patient(request):
        """
        View for a doctor to discharge a patient from the hospital that the doctor is working at
        :return: redirects to a template or another view
        """
        if (not request.user.is_authenticated()) or request.user.first_name != 'doctor':
            raise Http404
        else:
            if request.method == 'POST':
                if 'cancel' in request.POST:
                    return redirect('index')
                form = DischargePatientForm(request.POST, user=request.user)
                if form.is_valid():
                    patient = User.objects.get(username=request.POST.get('patient'))
                    profileInfo = patient.patient_user_profile

                    prev_hospital = profileInfo.current_hospital
                    stats = SysStats.objects.get(hospital=prev_hospital)
                    admissionInfo = AdmissionInfo()
                    admissionInfo.patient = patient
                    admissionInfo.admission_time = profileInfo.admission_time
                    admissionInfo.discharge_time = timezone.now()
                    admissionInfo.save()
                    stats.admissions.add(admissionInfo)
                    stats.save()
                    profileInfo.admission_time = timezone.now()

                    profileInfo.current_hospital = None
                    profileInfo.save()
                    message = 'Patient: {} {} discharged from Hospital {}'.format(profileInfo.first_name,
                                                                               profileInfo.last_name, prev_hospital)

                    # log entry creation/save
                    log_user = request.user
                    log_message = "Patient discharged"
                    log = LogEntry(user=log_user, message=log_message, time=timezone.now())
                    log.save()

                    return render(request, 'return_home_message.html', {'message': message, 'url': 'index'})
            else:
                form = DischargePatientForm(user=request.user)
            return render(request, 'form_generic.html', {'form': form, 'title': 'Discharge Patient'})



class PrivateMessage(generic.ListView):
    def view_messages(request):
        """
        View for any user to be able to view their inbox of private messages
        :return: redirects to a template or another view
        """

        if (not request.user.is_authenticated()):
            raise Http404
        if request.method == 'POST':
            if ('create' in request.POST):
                return redirect('create_message', None)
            form = ViewMessagesForm(request.POST, user=request.user)
            if form.is_valid():
                message = request.POST.get('message')
                return redirect('read_message', message)
        else:
            form = ViewMessagesForm(user=request.user)
        return render(request, 'view_messages.html', {'form': form, 'title': 'View Messages'})


    def create_message(request, receiver):
        """
        View for any user to be able to create a private message and send it to another user
        :param receiver: Used to auto-fill receiver field, if the user is replying to a message then this will be the sender of the message he is replying to
        :return: redirects to a template or another view
        """
        if (not request.user.is_authenticated()):
            raise Http404
        if request.method == 'POST':
            if ('cancel' in request.POST):
                return redirect('view_messages')
            form = CreateMessageForm(request.POST, user=request.user, receiver=receiver)
            if (form.is_valid()):
                privateMessage = form.save(commit=False)
                privateMessage.sender = request.user
                privateMessage.receiver = User.objects.get(username=request.POST.get('receiver_field'))
                privateMessage.created_at = datetime.now().strftime('%H:%M:%S')
                privateMessage.save()
                returnMessage = 'Private message sent'
                return render(request, 'return_home_message.html', {'message': returnMessage, 'url': 'view_messages'})
        else:
            form = CreateMessageForm(user=request.user, receiver=receiver)
        return render(request, 'form_generic.html', {'form': form, 'title': 'Create Message'})


    def read_message(request, message):
        """
        View for any user to be able to read the entire contents of a message that they have been sent
        :param message: Message for the user to read
        :return: redirects to a template or another view
        """
        if (not request.user.is_authenticated()):
            raise Http404
        if request.method == 'POST':
            if ('back' in request.POST):
                return redirect('view_messages')
            if('reply' in request.POST):
                receiver = request.POST.get('sender_field')
                return redirect('create_message', receiver)
        form = ReadMessageForm(instance=request.user.receiver.get(id = message))
        return render(request, 'read_message.html', {'form': form, 'title': 'Read Message'})


class Prescription(generic.ListView):
    """
    Class to create, view, and edit prescriptions
    """
    def create_prescriptions(request, patient):
        """
        Create a prescription and add it to the database
        :return: redirects user to the create prescription template or to home
        """

        if (not request.user.is_authenticated()):
            raise Http404
        if (request.user.first_name == 'nurse'):
            user = request.user.nurse_user_profile.current_doctor
        else:
            user = request.user

        if request.method == "POST":
            if "cancel" in request.POST:
                return redirect('index')
            form = CreatePrescriptionsForm(request.POST, hospital=user.hospital_set.all(), user=user) # ***PLACEHOLDER***
            if user.first_name == 'doctor':
                doctor = user
                #patient = request.POST.get('patient')
            #doctor = request.POST.get('doctor')
            #patient = request.POST.get('patient')

            if form.is_valid(doctor=doctor, patient=patient, name=request.POST.get('name'), notes=request.POST.get('notes'), this=None):
                post = form.save(commit=False)
                #print(post)
                if user.first_name == 'doctor':
                    patient = User.objects.get(username=patient)
                post.associated_patient = patient
                post.associated_doctor = doctor
                print("Doc: ", post.associated_doctor)
                print("Patient: ", post.associated_patient)

                #ask???
                #post.month = post.date.month
                #post.year = post.date.year
                #post.day = post.date.day
                #post.name = request.POST.get('name')
                #post.notes = request.POST.get('notes')
                #post.save()
                post.associated_patient = patient
                post.save()

                return render(request, 'return_home_message.html', {'message': 'Prescription Added', 'url': 'index'})
        else:
            form = CreatePrescriptionsForm(hospital=user.hospital_set.all(), user=user) # ***PLACEHOLDER***
        return render(request, 'form_generic.html', {'form': form, 'title': 'Add Prescription'})


    def view_prescriptions(request, patient):
        if (not request.user.is_authenticated()) or request.user.first_name != 'patient':
            raise Http404
        if patient == "None":
            patient = request.user
        #print("Patient: ", type(patient))
        #print("User: ", request.user)
        prescriptions = Prescriptions.objects.filter(associated_patient=patient)
        return render(request, 'view_prescriptions.html',
                      {'title': 'View Prescriptions', 'user': request.user, 'prescriptions': prescriptions})


        #   if form.is_valid():
        #       form.save(commit=False)
        #       profileInfo = request.user.patient_user_profile
        #       basicInfo = OrderedDict()
        #       basicInfo['Prescriptions'] = profileInfo.prescriptions
        #       basicInfo['Test Results'] = profileInfo.test_results
        #else:
        #    patient = request.user.patient_user_profile
        #    form = PatientPrescriptionsForm(instance=patient)
        #return render(request, 'view_prescriptions.html', {'form': form})
    """
    def view_prescriptions(request):  # , appointments_date):

        if (not request.user.is_authenticated()):
            raise Http404
        if (request.user.first_name == 'nurse'):
            user = request.user.nurse_user_profile.current_doctor
        else:
            user = request.user

        if (user.first_name == 'doctor'):
            prescriptions_list = user.doctor_prescriptions
            name = "{} {}".format(user.doctor_user_profile.first_name, user.doctor_user_profile.last_name)
        else:
            prescriptions_list = user.patient_prescriptions
            name = "{} {}".format(user.patient_user_profile.first_name, user.patient_user_profile.last_name)

        if request.method == 'POST':
            if 'back' in request.POST:
                return redirect('index')
            if 'delete' in request.POST:
                form = ViewPrescriptionsForm(request.POST, user=user)
                if form.is_valid():
                    prescriptions_list.filter(id=request.POST.get('prescriptions')).delete()
                form = ViewPrescriptionsForm(user=user)
            elif 'create' in request.POST:
                return redirect('create_appointment')
            else:
                # print(request.user.patient_user_profile)
                form = ViewPrescriptionsForm(request.POST, user=user)
                if form.is_valid():
                    appointment = prescriptions_list.get(id=request.POST.get('appointments'))
                    request.method = 'GET'
                    return redirect('update_prescriptions', appointment, user)
        else:
            form = ViewPrescriptionsForm(user=user)
            try:
                a = prescriptions_list.all()  # pk=appointments_date)
            except Exception as e:
                print(e)
                a = None
        return render(request, 'prescriptions/prescriptions.html', {'form': form, 'name': name,
                                                             'user': request.user})  # in this case, user is the literal user of the program who is logged in
    """
    def edit_prescriptions(request, patient, prescriptions):
        if request.user.first_name != 'doctor':
            raise Http404
        if request.method == 'POST':
            if 'cancel' in request.POST:
                 return redirect('view_prescriptions', patient)
            form = EditPrescriptionsForm(request.POST)
            if form.is_valid():
                testPost = form.save(commit=False)
                testPost.patient = User.objects.get(username=patient)
                profileInfo = request.user.doctor_user_profile
                name = "{} {}".format(profileInfo.first_name, profileInfo.last_name)
                testPost.doctor = name
                if prescriptions == 'None':
                    message = 'Prescription Created'
                else:
                    testPost.id = prescriptions
                    message = 'Prescription Updated'
                testPost.save()

                # log entry creation/save
                log_user = request.user
                log_message = "Edited prescription"
                log = LogEntry(user=log_user, message=log_message, time=timezone.now())
                log.save()

                return render(request, 'return_home_message.html', {'message': message, 'url': 'index'})
        else:
            if prescriptions == 'None':
                form = EditPrescriptionsForm()
            else:
                form = EditPrescriptionsForm(instance=Test.objects.get(id=prescriptions))
        if prescriptions == 'None':
            title = 'New Prescription'
        else:
            title = 'Update Test'
        return render(request, 'form_generic.html', {'form': form, 'title': title})



class Tests(generic.ListView):

    def view_tests(request, patient):
        """
        View the tests for a patient
        :param patient: patient to view tests for, if it is 'None', then it is set to the current user
        :return: redirects to template or to another view
        """
        if (not request.user.is_authenticated()) or (request.user.first_name == 'patient' and patient != 'None')\
                or (request.user.first_name == 'doctor' and patient == 'None')\
                or (request.user.first_name != 'patient' and request.user.first_name != 'doctor'):
            raise Http404
        isDoctor = (patient != 'None')
        if patient == 'None':
            patient = request.user
        if request.method == 'POST':
            if ('create' in request.POST):
                return redirect('edit_test', patient, 'None')
            if ('back' in request.POST):
                if not isDoctor:
                    return redirect('index')
                else:
                    return redirect('select_patient', 'view_tests')
            form = ViewTestsForm(request.POST, patient=patient)
            if form.is_valid():
                if ('delete' in request.POST):
                    Test.objects.filter(id=request.POST.get('test')).delete()
                    return redirect('view_tests', patient)

                test = request.POST.get('test')
                if not isDoctor:
                    return redirect('read_test', test)
                else:
                    return redirect('edit_test', patient, test)
        else:
            form = ViewTestsForm(patient=patient)
        profileInfo = User.objects.get(username=patient).patient_user_profile
        name = "{} {}".format(profileInfo.first_name, profileInfo.last_name)
        return render(request, 'view_tests.html', {'form': form, 'title': 'View Tests', 'user': request.user, 'name': name})


    def edit_test(request, patient, test):
        """
        A doctor can edit or update a patient's test
        :param patient: patient who the test is for
        :param test: the test to be updated (if it is 'None' then a new test will be created)
        :return: redirects to a template or another view
        """
        if request.user.first_name != 'doctor':
            raise Http404
        if request.method == 'POST':
            if ('cancel' in request.POST):
                return redirect('view_tests', patient)
            form = EditTestForm(request.POST)
            if (form.is_valid()):
                testPost = form.save(commit=False)
                testPost.patient = User.objects.get(username=patient)
                profileInfo = request.user.doctor_user_profile
                name = "{} {}".format(profileInfo.first_name, profileInfo.last_name)
                testPost.doctor = name
                if(test == 'None'):
                    message = 'Test Created'
                else:
                    testPost.id = test
                    message = 'Test Updated'
                testPost.save()

                # log entry creation/save
                log_user = request.user
                log_message = "Edited test"
                log = LogEntry(user=log_user, message=log_message, time=timezone.now())
                log.save()

                return render(request, 'return_home_message.html', {'message': message, 'url': 'index'})
        else:
            if test == 'None':
                form = EditTestForm()
            else:
                form = EditTestForm(instance=Test.objects.get(id=test))
        if test == 'None':
            title = 'New Test'
        else:
            title = 'Update Test'
        return render(request, 'form_generic.html', {'form': form, 'title': title})


    def read_test(request, test):
        """
        A patient can read more info about a test
        :param test: test that the patient wants to read about
        :return: redirects to a template or another view
        """
        if request.user.first_name != 'patient':
            raise Http404
        if request.method == 'POST':
            if ('back' in request.POST):
                return redirect('view_tests', None)
        form = ReadTestForm(instance=Test.objects.get(id=test))

        # log entry creation/save
        log_user = request.user
        log_message = "Read test"
        log = LogEntry(user=log_user, message=log_message, time=timezone.now())
        log.save()

        return render(request, 'view_only.html', {'form': form, 'title': 'View Test'})

class GenericUser(generic.ListView):
    def select_patient(request, redirectUrl):
        """
        View for a doctor or a nurse ro select a patient and redirect to a url with that patient passed as a parameter
        :param redirectUrl: URL that the user will be redirected to upon choosing a patient
        :return: redirects to a template or another view
        """
        if request.user.first_name != 'nurse' and request.user.first_name != 'doctor':
            raise Http404
        if request.method == 'POST':
            form = SelectPatientForm(request.POST, hospital=request.user.hospital_set.all()) # *** HOSPITAL SHOULD BE THE HOSPITAL THE NURSE WORKS IN, ONCE HOSPITAL IS IMPLEMENTED ***
            if "cancel" in request.POST:
                return redirect('index')
            if form.is_valid():
                patient = request.POST.get('patient')
                #print(patient)
                return redirect(redirectUrl, patient)
        else:
            form = SelectPatientForm(hospital=request.user.hospital_set.all())
        return render(request, 'select_form.html', {'form': form, 'title': 'Select Patient'})

    def edit_medical_info(request, patient):
        """
        View for a nurse or a doctor to be able to edit a patient's medical information
        :param patient: patient whose medical info the user is editing
        :return: redirects to a template or another view
        """
        if request.user.first_name != 'nurse' and request.user.first_name != 'doctor':
            raise Http404
        if request.method == 'POST':
            form = EditMedicalInfoForm(request.POST) # *** HOSPITAL SHOULD BE THE HOSPITAL THE NURSE WORKS IN, ONCE HOSPITAL IS IMPLEMENTED ***
            if "cancel" in request.POST:
                return redirect('index')
            patientProfile = User.objects.get(username=patient).patient_user_profile
            if form.is_valid():
                medicalInfo = form.save(commit=False)
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
        """
        View for a doctor or a nurse to admit a patient to the hospital that he works at
        :return: redirects to a template or another view
        """
        if request.user.first_name != 'nurse' and request.user.first_name != 'doctor':
            raise Http404
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

                prev_hospital = profileInfo.current_hospital
                if prev_hospital != None:
                    stats = SysStats.objects.get(hospital=prev_hospital)
                    admissionInfo = AdmissionInfo()
                    admissionInfo.patient = patient
                    admissionInfo.admission_time = profileInfo.admission_time
                    admissionInfo.discharge_time = timezone.now()
                    admissionInfo.statistics = stats
                    admissionInfo.save()
                    stats.save()

                profileInfo.admission_time = timezone.now()

                profileInfo.current_hospital = hospital
                profileInfo.save()
                message = 'Patient: {} {} admitted to Hospital: {}'.format(profileInfo.first_name, profileInfo.last_name, hospital)

                # log entry creation/save
                log_user = request.user
                log_message = "Patient admitted"
                log = LogEntry(user=log_user, message=log_message, time=timezone.now())
                log.save()

                return render(request, 'return_home_message.html', {'message': message, 'url': 'index'})
        else:
            form = AdmitPatientForm(user=request.user)
        return render(request, 'form_generic.html', {'form': form, 'title': 'Admit Patient'})


class Log(generic.ListView):

    def view_log(request):
        if (request.user.first_name) != 'admin':
            raise Http404

        log = LogEntry.objects.all()
        return render(request, 'view_log.html', {'log': log})

class SystemStatistics(generic.ListView):
    def view_statistics(request):
        if (request.user.first_name) != 'admin':
            raise Http404
        if request.method == 'POST':
            if ('back' in request.POST):
                return redirect('index')
            form = ViewStatisticsForm( user=request.user, choice=request.POST.get('hospital'))
        else:
            form = ViewStatisticsForm(user=request.user, choice=0)
        return render(request, 'view_only.html', {'form': form, 'title': 'View Statistics'})
