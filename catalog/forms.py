from django import forms
from django.contrib.auth.models import User

from .models import *

class PatientRegisterProfileForm(forms.ModelForm):

    class Meta:
        model = PatientProfileInfo
        fields = (
        'first_name', 'last_name', 'phone_number', 'insurance', 'pref_hospital', 'emergency_contact_first_name', 'emergency_contact_last_name', 'emergency_contact_email', 'medical_info')


class PatientRegisterUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PatientRegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['password'] = forms.CharField(widget = widgets.PasswordInput)
        self.fields['re_enter_password'] = forms.CharField(widget=widgets.PasswordInput)
    class Meta:
        model = PatientRegisterInfo
        fields = (
        'username', 'password','re_enter_password', 'email')

    def clean(self):
        cleaned_data = self.cleaned_data  # individual field's clean methods have already been called
        password1 = cleaned_data.get("password")
        password2 = cleaned_data.get("re_enter_password")
        username = cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError({'username': ["Username already in use", ]})
        if password1 != password2:
            raise forms.ValidationError({'password': ["Passwords must be identical",]})

        return cleaned_data

    """def clean_username(self, user):
        cleaned_data = self.cleaned_data  # individual field's clean methods have already been called
        username = cleaned_data.get("password")
        if password1 != password2:
            raise forms.ValidationError({'password': ["Passwords must be identical",]})

        return cleaned_data
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(PatientRegisterUserForm, self).__init__(*args, **kwargs)
        self.clean_username(self, user)
        self.appointments = user.patient.all()
        choices = []
        for i, appointment in enumerate(self.appointments):
            choices.append((appointment, 'Appointment: {}, on {}, at {}'.format(appointment.title, appointment.date, appointment.time)))
        self.fields['appointments'] = forms.ChoiceField(choices=choices, widget=forms.RadioSelect)"""

class PatientUpdateBasicInfoForm(forms.ModelForm):

    class Meta:
        model = PatientProfileInfo
        fields = (
            'first_name', 'last_name', 'phone_number','insurance', 'pref_hospital', 'emergency_contact_first_name', 'emergency_contact_last_name', 'emergency_contact_email',
        )