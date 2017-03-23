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
    return AppointmentCalendar.calendar(request, datetime.now().year,datetime.now().month)

class PatientRegistration(generic.ListView):
    template_name = 'registration/patient_registration.html'

    def register(request):
        if request.method == "POST":
            if "cancel" in request.POST:
                return redirect('index')
            form = RegisterUserForm(request.POST)
            form2 = RegisterPatientForm(request.POST);
            if all([form.is_valid(), form2.is_valid()]) and not User.objects.filter(username=request.POST.get('username')).exists():
                userInfo = form.save(commit=False)
                userInfo.save()
                #User.objects.all().delete()

                user = User.objects.create_user(username = request.POST.get("username"), password = request.POST.get("password"), email = request.POST.get('email'), first_name = 'patient')

                profileInfo = form2.save(commit=False)
                profileInfo.user = user
                profileInfo.save()
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

                return render(request, 'return_home_message.html', {'message': message, 'url': 'index'})
        else:
            form = RegisterUserForm()
            form2 = RegisterPatientForm()
        return render(request, '../templates/registration/patient_registration.html', {'form': form, 'form2': form2})

class PatientProfile(generic.edit.CreateView):

    def view(request):
        if request.method == "POST":

            if "update" in request.POST:
                print(request.POST)
                return redirect('patient_profile_update')
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
        #print("hi")
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
                return render(request, 'return_home_message.html', {'message': message, 'url': 'index'})
               #patient.first_name = request.POST.get("first_name")
        else:
            patient = request.user.patient_user_profile
            form = PatientUpdateBasicInfoForm(instance = patient)
        return render(request, 'patient_update_profile.html', {'form': form})

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
		
    def calendar(request, year, month):	
        cal = AppointmentCalendar(request.user.patient_appointment.filter(month=month, year=year)).formatmonth(year, month)
        #cal = HTMLCalendar(firstweekday=0).formatmonth(year, month)
        return render(request, 'calendar.html', {'calendar': mark_safe(cal),})

def view_syslog(request):
    if request.user.is_superuser:
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
                message = "Admin successfully added"
                return render(request, 'return_home_message.html', {'message': message, 'url': 'index'})
        else:
            form = RegisterUserForm()
            form2 = RegisterAdminForm()
        return render(request, '../templates/registration/patient_registration.html', {'form': form, 'form2': form2})

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
                #print(user.doctor_user_profile)
                message = "Doctor successfully added"
                return render(request, 'return_home_message.html', {'message': message, 'url': 'index'})
        else:
            form = RegisterUserForm()
            form2 = RegisterDoctorForm()
        return render(request, '../templates/registration/patient_registration.html', {'form': form, 'form2': form2})

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
                message = "Nurse successfully added"
                return render(request, 'return_home_message.html', {'message': message, 'url': 'index'})
        else:
            form = RegisterUserForm()
            form2 = RegisterNurseForm()
        return render(request, '../templates/registration/patient_registration.html', {'form': form, 'form2': form2})



class Nurse(generic.ListView):

    def select_doctor(request):
        """
        Display a list of doctors in the hospital that the nurse works in
        Allow the nurse to choose a specific doctor and the nurse's value for current doctor will be updated
        :return: redirects to a template
        """
        if request.method == 'POST':
            form = SelectDoctorForm(request.POST, hospital=None) # *** HOSPITAL SHOULD BE THE HOSPITAL THE NURSE WORKS IN, ONCE HOSPITAL IS IMPLEMENTED ***
            if form.is_valid():
                if "cancel" in request.POST:
                    return redirect('index')
                doctor = User.objects.get(username=request.POST.get('doctors'))
                request.method = 'GET'
                profileInfo = request.user.nurse_user_profile
                profileInfo.current_doctor = doctor
                profileInfo.save()
                message = 'Current doctor is now: {} {}'.format(doctor.doctor_user_profile.first_name, doctor.doctor_user_profile.last_name)
                return render(request, 'return_home_message.html', {'message': message, 'url': 'index'})
        else:
            form = SelectDoctorForm(hospital=None)
        return render(request, 'form_generic.html', {'form': form, 'title': 'Select Doctor'})
