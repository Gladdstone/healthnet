from django.shortcuts import render, redirect
from django.views import generic
from .forms import *
from django.contrib.auth.models import User
from .models import *
from appointment.models import Appointment
from django.forms.formsets import formset_factory

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
            form = PatientRegisterUserForm(request.POST)
            form2 = PatientRegisterProfileForm(request.POST);
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
                    if emergency_contact != None and emergency_contact.user_profile.first_name == profileInfo.emergency_contact_first_name and \
                                emergency_contact.user_profile.last_name == profileInfo.emergency_contact_last_name: #checking if emergency contact info matches with patient in database
                        emergency_contact.patientprofileinfo_set.add(profileInfo)
                        profileInfo.save()
                        emergency_contact.save()
                    message = 'Emergency contact linked to existing patient'
                except Exception as err:
                    print("Exception {0}".format(err))
                    message = 'Emergency contact not linked to any existing patient'


                profileInfo.save()

                return render(request, 'return_home_message.html', {'message': message, 'url': 'index'})
        else:
            form = PatientRegisterUserForm()
            form2 = PatientRegisterProfileForm();
        return render(request, '../templates/registration/patient_registration.html', {'form': form, 'form2': form2})

class PatientProfile(generic.edit.CreateView):

    def view(request):
        if request.method == "POST":

            if "update" in request.POST:
                print(request.POST)
                return redirect('patient_profile_update')
        else:
            profileInfo = request.user.user_profile
            basicInfo = {'First name': profileInfo.first_name, 'Last name': profileInfo.last_name,
                        'Phone number': profileInfo.phone_number}
        return render(request, 'patient_view_profile.html', {'basicInfo': basicInfo})

    def update_basic(request):
        print("hi")
        if request.method == 'POST':
            if "cancel" in request.POST:
                return redirect('patient_profile')
            form = PatientUpdateBasicInfoForm(request.POST)
            if form.is_valid():
                form.save(commit=False)
                patient = request.user.user_profile
                for k, v in request.POST.items():
                    try:
                        setattr(patient, k, v)
                    except:
                        pass
                patient.save()
                return redirect('index')
               #patient.first_name = request.POST.get("first_name")
        patient = request.user.user_profile
        form = PatientUpdateBasicInfoForm(instance = patient)
        return render(request, 'patient_update_profile.html', {'form': form})

class AppointmentCalendar(HTMLCalendar):

    template_name = '/calendar.html'

    def __init__(self, appointments):
        super(AppointmentCalendar, self).__init__()
        self.appointments = self.group_by_day(appointments)

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.appointments:
                cssclass += ' filled'
                body = ['<ul>']
                for appointment in self.appointments[day]:
                    body.append('<li>')
                    body.append('<a href="%s">' % appointment.get_absolute_url())
                    body.append(esc(appointment.title))
                    body.append('</a></li>')
                body.append('</ul>')
                return self.day_cell(cssclass, '%d %s' % (day, ''.join(body)))
            return self.day_cell(cssclass, day)
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(AppointmentCalendar, self).formatmonth(year, month)

    def group_by_day(self, appointments):
        field = lambda appointment: appointment.performed_at.day
        return dict(
            [(day, list(items)) for day, items in groupby(appointment, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)
		
    def calendar(request, year, month):
        """my_appointments = Appointment.objects.order_by('my_date').filter(
        my_date__year=year, my_date__month=month)
        cal = AppointmentCalendar(my_appointments).formatmonth(year, month)"""
        #cal = AppointmentCalendar(Appointment.objects).formatmonth(2017, 3)
        cal = HTMLCalendar(firstweekday=0).formatmonth(year, month)
        return render_to_response('calendar.html', {'calendar': mark_safe(cal),})