from django import forms
from django.forms import extras
from django.contrib.admin import widgets
import datetime
from .models import Appointment, AppointmentSelect


class CreateAppointmentForm(forms.ModelForm):
    day = datetime.date.today()
    date = forms.DateField(widget=extras.SelectDateWidget, initial= day)
    doctor = forms.ChoiceField(choices=(('doctor_1', 'Doctor 1'), ('doctor_2', 'Doctor 2'),))
    class Meta:
        model = Appointment
        fields = ('title', 'date', 'time', 'doctor')
    def is_valid(self, **kwargs):
        user = kwargs.pop('user')
        title = kwargs.pop('title')
        date_month = kwargs.pop('date_month')
        date_year = kwargs.pop('date_year')
        date_day = kwargs.pop('date_day')
        time = kwargs.pop('time')
        valid = super(CreateAppointmentForm, self).is_valid()
        if not valid:
            return valid
        try:
            i = user.patient.filter(title=title)
            if (len(i) > 0):
                self._errors['title'] = ["Title must be unique"]
                return False
            d = user.patient.filter(month= date_month,
                                    year = date_year,
                                    day = date_day,
                                    time = time)
            print(d)
            if (len(d) > 0):
                self._errors['date'] = ["Date and time must be unique"]
                return False
            return True
        except Exception as e:
            return True

        #fields = ('title', 'date')
    """def __init__(self, *args, **kwargs):
        super(CreateAppointmentForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget = widgets.AdminDateWidget()
        #self.fields['mytime'].widget = widgets.AdminTimeWidget()
        #self.fields['mydatetime'].widget = widgets.AdminSplitDateTime()"""

class ChooseAppointmentForm(forms.Form):
    """def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChooseAppointmentForm, self).__init__(*args, **kwargs)
        self.choices = self.user.patient.all()
        #self.fields['appt'].choices = self.choices
        #self.fields['appt'].widget = forms.RadioSelect()
        appt = forms.RadioSelect(choices=self.choices)

    class Meta:
        model = AppointmentSelect
        fields = ('appt',)"""


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ChooseAppointmentForm, self).__init__(*args, **kwargs)
        self.appointments = user.patient.all()
        choices = []
        for i, appointment in enumerate(self.appointments):
            choices.append((appointment, 'Appointment: {}, on {}, at {}'.format(appointment.title, appointment.date, appointment.time)))
        self.fields['appointments'] = forms.ChoiceField(choices=choices, widget=forms.RadioSelect)
