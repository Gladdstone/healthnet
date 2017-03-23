from django import forms
from django.contrib.auth.models import User

from .models import *

class RegisterPatientForm(forms.ModelForm):
    """
    Form to register a patient
    """
    class Meta:
        model = Patient
        fields = (
        'first_name', 'last_name', 'phone_number', 'insurance', 'pref_hospital', 'emergency_contact_first_name', 'emergency_contact_last_name', 'emergency_contact_email', 'medical_info')

class RegisterAdminForm(forms.ModelForm):
    """
    Form to register an Admin
    """
    class Meta:
        model = Admin
        fields = (
        'first_name', 'last_name')

class RegisterDoctorForm(forms.ModelForm):
    """
    Form to register a Doctor
    """
    class Meta:
        model = Doctor
        fields = (
        'first_name', 'last_name')

class RegisterNurseForm(forms.ModelForm):
    """
    Form to register a Nurse
    """
    class Meta:
        model = Nurse
        fields = (
        'first_name', 'last_name')


class RegisterUserForm(forms.ModelForm):
    """
    Form to register a User (used in the backend of all the other classes because they have a one to one key with a User)
    """
    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['password'] = forms.CharField(widget = widgets.PasswordInput)
        self.fields['re_enter_password'] = forms.CharField(widget=widgets.PasswordInput)
    class Meta:
        model = UserInfo
        fields = (
        'username', 'password','re_enter_password', 'email')

    def clean(self):
        """
        Basically, makes sure that the passwords are the same and the Username is unique
        :return: cleaned_data to keep original functionality of clean
        """
        cleaned_data = self.cleaned_data  # individual field's clean methods have already been called
        password1 = cleaned_data.get("password")
        password2 = cleaned_data.get("re_enter_password")
        username = cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError({'username': ["Username already in use", ]})
        if password1 != password2:
            raise forms.ValidationError({'password': ["Passwords must be identical",]})

        return cleaned_data


class PatientUpdateBasicInfoForm(forms.ModelForm):
    """
    Form to update a patient's basic info
    """
    class Meta:
        model = Patient
        fields = (
            'first_name', 'last_name', 'phone_number','insurance', 'pref_hospital', 'emergency_contact_first_name', 'emergency_contact_last_name', 'emergency_contact_email',
        )

class SelectDoctorForm(forms.Form):
    """
    Form to display a list of all the doctors in a specified hospital and allow a nurse to select one to be his current doctor
    """
    def __init__(self, *args, **kwargs):
        hospital = kwargs.pop('hospital')
        super(SelectDoctorForm, self).__init__(*args, **kwargs)
        self.doctors = User.objects.filter(first_name='doctor')
        choices = []
        for i, doctor in enumerate(self.doctors):
            choices.append((doctor, 'Doctor: {} {}'.format(doctor.doctor_user_profile.first_name, doctor.doctor_user_profile.last_name)))
        self.fields['doctors'] = forms.ChoiceField(choices=choices, widget=forms.RadioSelect)