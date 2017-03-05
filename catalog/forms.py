from django import forms

from .models import PatientProfileInfo, PatientRegisterInfo

class PatientRegisterProfileForm(forms.ModelForm):

    class Meta:
        model = PatientProfileInfo
        fields = (
        'first_name', 'last_name', 'phone_number', 'insurance', 'pref_hospital', 'emergency_contact', 'medical_info')

class PatientRegisterUserForm(forms.ModelForm):

    class Meta:
        model = PatientRegisterInfo
        fields = (
        'username', 'password', 'email')

class PatientUpdateBasicInfoForm(forms.ModelForm):

    class Meta:
        model = PatientProfileInfo
        fields = (
            'first_name', 'last_name', 'phone_number'
        )