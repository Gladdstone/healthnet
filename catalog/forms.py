from django import forms

from .models import *

class PatientRegisterProfileForm(forms.ModelForm):

    class Meta:
        model = PatientProfileInfo
        fields = (
        'first_name', 'last_name', 'phone_number', 'insurance', 'pref_hospital', 'emergency_contact_first_name', 'emergency_contact_last_name', 'emergency_contact_email', 'medical_info')


class PatientRegisterUserForm(forms.ModelForm):

    class Meta:
        model = PatientRegisterInfo
        fields = (
        'username', 'password', 'email')

class PatientUpdateBasicInfoForm(forms.ModelForm):

    class Meta:
        model = PatientProfileInfo
        fields = (
            'first_name', 'last_name', 'phone_number',
        )