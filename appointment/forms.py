from django import forms

from .models import Appointment


class CreateAppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = ('date', 'time', 'doctor') #'doctor')
