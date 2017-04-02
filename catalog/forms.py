import operator

from django import forms
from django.contrib.auth.models import User
from django.forms import extras
from django.utils import timezone

from .models import *

class RegisterPatientForm(forms.ModelForm):
    """
    Form to register a patient
    """
    class Meta:
        model = Patient
        fields = (
        'first_name', 'last_name', 'phone_number', 'insurance', 'pref_hospital', 'emergency_contact_first_name', 'emergency_contact_last_name', 'emergency_contact_email')

    def __init__(self, *args, **kwargs):
        super(RegisterPatientForm, self).__init__(*args, **kwargs)
        hospitals = Hospital.objects.all()
        choices = []
        for i, hospital in enumerate(hospitals):
            choices.append((hospital, '{}'.format(hospital)))
        self.fields['pref_hospital'] = forms.ChoiceField(choices=choices)


class PatientMedicalInfoForm(forms.ModelForm):
    """
    Form for a patient to fill out when he registers
    """
    EYE_COLOR_CHOICES = (
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('brown', 'Brown'),
        ('hazel', 'Hazel')
    )
    RACE_CHOICES = (
        ('native_american', 'American Indian or Alaska Native'),
        ('asian', 'Asian'),
        ('black', 'Black or African America'),
        ('hispanic', 'Hispanic or Latino'),
        ('white', 'White or Caucasian')
    )
    SEX_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female')
    )

    class Meta:
        model = MedicalInfo
        fields = ('height', 'weight', 'eye_color', 'birthday', 'race', 'sex')

    def __init__(self, *args, **kwargs):
        super(PatientMedicalInfoForm, self).__init__(*args, **kwargs)
        self.fields['eye_color'] = forms.ChoiceField(choices=self.EYE_COLOR_CHOICES)
        self.fields['race'] = forms.ChoiceField(choices=self.RACE_CHOICES)
        self.fields['sex'] = forms.ChoiceField(choices=self.SEX_CHOICES)
        self.fields['birthday'] = forms.DateField(widget=extras.SelectDateWidget(years=range(datetime.datetime.now().year-150, datetime.datetime.now().year)))

class RegisterAdminForm(forms.ModelForm):
    """
    Form to register an Admin
    """
    class Meta:
        model = Admin
        fields = (
        'first_name', 'last_name', 'hospital')

    def __init__(self, *args, **kwargs):
        super(RegisterAdminForm, self).__init__(*args, **kwargs)
        hospitals = Hospital.objects.all()
        choices = []
        for i, hospital in enumerate(hospitals):
            choices.append((hospital, '{}'.format(hospital)))
        self.fields['pref_hospital'] = forms.ChoiceField(choices=choices)

class RegisterDoctorForm(forms.ModelForm):
    """
    Form to register a Doctor
    """
    class Meta:
        model = Doctor
        fields = (
        'first_name', 'last_name', 'hospital')

    def __init__(self, *args, **kwargs):
        super(RegisterDoctorForm, self).__init__(*args, **kwargs)
        hospitals = Hospital.objects.all()
        choices = []
        for i, hospital in enumerate(hospitals):
            choices.append((hospital, '{}'.format(hospital)))
        self.fields['pref_hospital'] = forms.ChoiceField(choices=choices)

class RegisterNurseForm(forms.ModelForm):
    """
    Form to register a Nurse
    """
    class Meta:
        model = Nurse
        fields = (
        'first_name', 'last_name', 'hospital')

    def __init__(self, *args, **kwargs):
        super(RegisterNurseForm, self).__init__(*args, **kwargs)
        hospitals = Hospital.objects.all()
        choices = []
        for i, hospital in enumerate(hospitals):
            choices.append((hospital, '{}'.format(hospital)))
        self.fields['pref_hospital'] = forms.ChoiceField(choices=choices)


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
            'first_name', 'last_name', 'phone_number','insurance', 'emergency_contact_first_name', 'emergency_contact_last_name', 'emergency_contact_email',
        )

class changePassword(forms.ModelForm):
    """
    Form to update a password
    """
    class Meta:
        model = User
        fields = (
            'password',
        )

class SelectDoctorForm(forms.Form):
    """
    Form to display a list of all the doctors in a specified hospital and allow a nurse to select one to be his current doctor
    """
    def __init__(self, *args, **kwargs):
        hospitals = kwargs.pop('hospital')
        super(SelectDoctorForm, self).__init__(*args, **kwargs)
        doctors = []
        for i, hospital in enumerate(hospitals):
            doctors += hospital.people.filter(first_name='doctor')

        doctors = list(set(doctors))  # remove duplicates for users that are in more than one hospital

        choices = []
        for i, doctor in enumerate(doctors):
            choices.append((doctor, 'Doctor: {} {}'.format(doctor.doctor_user_profile.first_name, doctor.doctor_user_profile.last_name)))
        self.fields['doctors'] = forms.ChoiceField(choices=choices, widget=forms.RadioSelect)


class SelectPatientForm(forms.Form):
    """
    Form to display a list of all the doctors in a specified hospital and allow a nurse to select one to be his current doctor
    """
    def __init__(self, *args, **kwargs):
        hospitals = kwargs.pop('hospital')
        super(SelectPatientForm, self).__init__(*args, **kwargs)
        patients = []
        for i, hospital in enumerate(hospitals):
            patients += hospital.people.filter(first_name='patient')

            patients = list(set(patients))  # remove duplicates for users that are in more than one hospital


        choices = []
        for i, patient in enumerate(patients):
            choices.append((patient, '{} {}'.format(patient.patient_user_profile.first_name, patient.patient_user_profile.last_name)))
        self.fields['patient'] = forms.ChoiceField(choices=choices)


class ReadMessageForm(forms.ModelForm):
    """

    """
    class Meta:
        model = PrivateMessage
        fields = ('sender_field', 'receiver_field', 'message_content')

    def __init__(self, *args, **kwargs):
        super(ReadMessageForm, self).__init__(*args, **kwargs)
        self.fields['sender_field'] = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
        self.fields['receiver_field'] = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
        self.fields['message_content'] = forms.CharField(widget=forms.Textarea(attrs={'readonly':'readonly', 'rows': 5, 'cols': 40, 'style': 'resize:none;'}))

class ViewMessagesForm(forms.Form):
    """

    """


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ViewMessagesForm, self).__init__(*args, **kwargs)
        messages = user.receiver.all()
        messages = sorted(messages, key=operator.attrgetter('created_at'), reverse=True)

        choices = []
        for i, message in enumerate(messages):
            sender = message.sender
            if (sender.first_name == 'doctor'):
                profileInfo = sender.doctor_user_profile
            elif (sender.first_name == 'nurse'):
                profileInfo = sender.nurse_user_profile
            elif (sender.first_name == 'admin'):
                profileInfo = sender.admin_user_profile
            else:
                profileInfo = sender.patient_user_profile
            choices.append((message, 'From: {} {} At: {}'.format(profileInfo.first_name, profileInfo.last_name,
                                                           message.created_at)))
        self.fields['message'] = forms.ChoiceField(label="", choices=choices, widget=forms.RadioSelect(attrs={"onChange":'submit()'}))

class CreateMessageForm(forms.ModelForm):
    """

    """

    class Meta:
        model = PrivateMessage
        fields = ('sender_field', 'receiver_field', 'message_content')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        receiver = kwargs.pop('receiver')
        hospitals = (User.objects.get(username=user).hospital_set.all())
        peoples = []
        for i, hospital in enumerate(hospitals):
            peoples += hospital.people.all()

        peoples = list(set(peoples)) # remove duplicates for users that are in more than one hospital

        choices = []
        for i, person in enumerate(peoples):
            if(person.first_name == 'doctor'):
                profileInfo = person.doctor_user_profile
            elif(person.first_name == 'nurse'):
                profileInfo = person.nurse_user_profile
            elif(person.first_name == 'admin'):
                profileInfo = person.admin_user_profile
            else:
                profileInfo = person.patient_user_profile

            choices.append((person, '{} {}, Username: {}'.format(profileInfo.first_name, profileInfo.last_name, person)))
        super(CreateMessageForm, self).__init__(*args, **kwargs)
        if (user.first_name == 'doctor'):
            profileInfo = user.doctor_user_profile
        elif (user.first_name == 'nurse'):
            profileInfo = user.nurse_user_profile
        elif (user.first_name == 'admin'):
            profileInfo = user.admin_user_profile
        else:
            profileInfo = user.patient_user_profile
        self.fields['sender_field'] = forms.CharField(initial='{}'.format(user), widget=forms.TextInput(attrs={'readonly':'readonly'}))
        self.fields['receiver_field'] = forms.ChoiceField(choices=choices, initial=receiver)
        self.fields['message_content'] = forms.CharField()

class AddHospitalForm(forms.ModelForm):
    """

    """

    class Meta:
        model = Hospital
        fields = ('name',)


class TransferPatientForm(forms.Form):
    """

    """

    def __init__(self, *args, **kwargs):
        super(TransferPatientForm, self).__init__(*args, **kwargs)

        patients = User.objects.filter(first_name='patient')
        choices = []
        for i, patient in enumerate(patients):
            profileInfo = patient.patient_user_profile
            choices.append((patient, '{} {}, Username: {}'.format(profileInfo.first_name, profileInfo.last_name, patient)))
        self.fields['patient'] = forms.ChoiceField(choices=choices)

        hospitals = Hospital.objects.all()
        choices = []
        for i, hospital in enumerate(hospitals):
            choices.append((hospital, '{}'.format(hospital)))
        self.fields['hospital'] = forms.ChoiceField(choices=choices)




class AdmitPatientForm(forms.Form):
    """

    """

    def __init__(self, *args, **kwargs):
        user = User.objects.get(username=kwargs.pop('user'))
        super(AdmitPatientForm, self).__init__(*args, **kwargs)

        patients = User.objects.filter(first_name='patient')
        choices = []
        for i, patient in enumerate(patients):
            profileInfo = patient.patient_user_profile
            choices.append((patient, '{} {}, Username: {}'.format(profileInfo.first_name, profileInfo.last_name, patient)))
        self.fields['patient'] = forms.ChoiceField(choices=choices)

        hospitals = user.hospital_set.all()
        choices = []
        for i, hospital in enumerate(hospitals):
            choices.append((hospital, '{}'.format(hospital)))
        self.fields['hospital'] = forms.ChoiceField(choices=choices)




class EditMedicalInfoForm(forms.ModelForm):
    heart_rate = forms.CharField(required=False)
    diastolic_blood_pressure = forms.CharField(required=False)
    systolic_blood_pressure = forms.CharField(required=False)

    class Meta:
        model = MedicalInfo
        fields = ('height', 'weight', 'heart_rate', 'diastolic_blood_pressure', 'systolic_blood_pressure')

