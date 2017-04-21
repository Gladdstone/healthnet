from django import forms
from django.forms import extras
from django.contrib.admin import widgets
from django.contrib.auth.models import User

import datetime

from catalog.models import Hospital
from .models import Appointment


class CreateAppointmentForm(forms.ModelForm):
    """
    Form for a user to create an appointment
    """
    day = datetime.date.today()
    date = forms.DateField(widget=extras.SelectDateWidget, initial= day)
    #doctor = forms.ChoiceField(choices=(('doctor_1', 'Doctor 1'), ('doctor_2', 'Doctor 2'),))
    class Meta:
        model = Appointment
        fields = ('title', 'date', 'time', 'doctor', 'patient', 'description')

    def __init__(self, *args, **kwargs):
        hospitals = (kwargs.pop('hospital').all())
        user = kwargs.pop('user')
        if (user.first_name == 'doctor'):
            name = "{} {}".format(user.doctor_user_profile.first_name, user.doctor_user_profile.last_name)
        else:
            name = "{} {}".format(user.patient_user_profile.first_name, user.patient_user_profile.last_name)

        super(CreateAppointmentForm, self).__init__(*args, **kwargs)

        if (user.first_name=='patient'):
            self.doctor = []
            for i, hospital in enumerate(hospitals):
                self.doctor += hospital.people.filter(first_name='doctor')
                print(hospital.people.filter(first_name='doctor'))
            choices = []
            for i, doc in enumerate(self.doctor):
                choices.append((doc, '{} {}'.format(doc.doctor_user_profile.first_name, doc.doctor_user_profile.last_name)))
            self.fields['doctor'] = forms.ChoiceField(choices=choices)
            self.fields['patient'] = forms.CharField(initial= user, widget=forms.TextInput(attrs={'readonly':'readonly'}))
            self.fields['patient'].required = False
        else:
            self.patient = []
            for i, hospital in enumerate(hospitals):
                self.patient += hospital.people.filter(first_name='patient')
            choices = []
            for i, pat in enumerate(self.patient):
                choices.append(
                    (pat, '{} {}'.format(pat.patient_user_profile.first_name, pat.patient_user_profile.last_name)))
            self.fields['doctor'] = forms.CharField(initial= user ,widget=forms.TextInput(attrs={'readonly':'readonly'}))
            self.fields['patient'] = forms.ChoiceField(choices=choices)
            self.fields['doctor'].required = False
        self.fields['description'] = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 40, 'style': 'resize:none;'}))
        self.fields['description'].label = 'Description or Symptoms (Optional)'

    def is_valid(self, **kwargs):
        doctor = User.objects.get(username=kwargs.pop('doctor'))
        patient = User.objects.get(username=kwargs.pop('patient'))
        #title = kwargs.pop('title')
        date_month = kwargs.pop('date_month')
        date_year = kwargs.pop('date_year')
        date_day = kwargs.pop('date_day')
        time = kwargs.pop('time')
        this = kwargs.pop('this')
        valid = super(CreateAppointmentForm, self).is_valid()


        #doctor = User.objects.get(username=self.cleaned_data['doctor'])
        #patient = User.objects.get(username=self.self.cleaned_data['patient'])

        if not valid:
            return valid
        try:

            """i = patient.patient_appointment.filter(id=title)
            j = doctor.doctor_appointment.filter(id=title)
            if (len(i) > 0 and (this==None or title != this.title)):
                self._errors['title'] = ["Patient already has appointment with that title"]
                return False
            elif (len(j) > 0 and (this==None or title != this.title)):
                self._errors['title'] = ["Doctor already has appointment with that title"]
                return False"""

            patient_appointments = patient.patient_appointment.filter(month= date_month,
                                    year = date_year,
                                    day = date_day,
                                    time = time)
            doctor_appointments = doctor.doctor_appointment.filter(month=date_month,
                                                                   year=date_year,
                                                                   day=date_day,
                                                                   time=time)


            if  (this!= None and date_month == str(this.month) and
                                        date_year == str(this.year) and
                                        date_day == str(this.day) and
                                        time == str(this.time)):
                pass
            elif (len(patient_appointments) > 0):

                self._errors['date'] = ["Patient already has an appointment at that time"]
                return False
            elif (len(doctor_appointments) > 0):
                self._errors['date'] = ["Doctor already has an appointment at that time"]
                return False
            return True
        except Exception as e:
            print(e);
            return True

        #fields = ('title', 'date')
    """def __init__(self, *args, **kwargs):
        super(CreateAppointmentForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget = widgets.AdminDateWidget()
        #self.fields['mytime'].widget = widgets.AdminTimeWidget()
        #self.fields['mydatetime'].widget = widgets.AdminSplitDateTime()"""

class ChooseAppointmentForm(forms.Form):
    """
    Form for a user to choose an appointment
    """
    def __init__(self, *args, **kwargs):
        """
        Finds all of a users appointments and adds them to the 'appointments' field
        :param args: default arguments passed to init
        :param kwargs: default keyword args passed to init as well as user, which defines who the appointment list is for
        """
        user = kwargs.pop('user')
        super(ChooseAppointmentForm, self).__init__(*args, **kwargs)
        if(user.first_name=='patient'):
            self.appointments = user.patient_appointment.all()
            appointment_partner = 'doctor' # patient is partnered with a doctor and vice versa
        else:
            self.appointments = user.doctor_appointment.all()
            appointment_partner = 'patient'
        choices = []

        for i, appointment in enumerate(self.appointments):
            partner_first_name = appointment.associated_patient.patient_user_profile.first_name if (appointment_partner=='patient') else appointment.associated_doctor.doctor_user_profile.first_name
            partner_last_name = appointment.associated_patient.patient_user_profile.last_name if (appointment_partner=='patient') else appointment.associated_doctor.doctor_user_profile.last_name
            choices.append((appointment, 'Appointment: {}, on {}, at {} with {} {}'
                            .format(appointment.title, appointment.date, appointment.time, partner_first_name, partner_last_name)))

        self.fields['appointments'] = forms.ChoiceField(label="", choices=choices, widget=forms.RadioSelect)
