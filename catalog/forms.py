import operator

from django import forms
from django.contrib.auth.models import User
from django.forms import extras
from django.utils import timezone

from catalog.utils import make_choice_list
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
        self.fields['hospital'] = forms.ChoiceField(choices=choices)


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
        self.fields['hospital'] = forms.ChoiceField(choices=choices)


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
        self.fields['hospital'] = forms.ChoiceField(choices=choices)


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


class CreatePrescriptionsForm(forms.ModelForm):
    """
    A form to create prescriptions
    """
    class Meta:
        model = Prescriptions
        fields = ('name', 'notes')#, 'patient')

    def __init__(self, *args, **kwargs):
        hospitals = (kwargs.pop('hospital').all())
        user = kwargs.pop('user')
        if (user.first_name == 'doctor'):
            name = "{} {}".format(user.doctor_user_profile.first_name, user.doctor_user_profile.last_name)
        else:
            name = "{} {}".format(user.patient_user_profile.first_name, user.patient_user_profile.last_name)

        super(CreatePrescriptionsForm, self).__init__(*args, **kwargs)

        """if user.first_name == 'patient':
            return None
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
            self.fields['doctor'].required = False"""
        self.fields['name'] = forms.CharField(widget=forms.Textarea())
        self.fields['notes'] = forms.CharField(widget=forms.Textarea())

    def is_valid(self, **kwargs):
        doctor = User.objects.get(username=kwargs.pop('doctor'))
        patient = User.objects.get(username=kwargs.pop('patient'))
        #title = kwargs.pop('title')
        p_name = kwargs.pop('name')
        p_notes = kwargs.pop('notes')
        this = kwargs.pop('this')
        valid = super(CreatePrescriptionsForm, self).is_valid()


        #doctor = User.objects.get(username=self.cleaned_data['doctor'])
        #patient = User.objects.get(username=self.self.cleaned_data['patient'])

        if not valid:
            return valid
        try:

            patient_prescriptions = patient.patient_prescriptions.filter(name=p_name, notes=p_notes)
            #doctor_prescriptions = doctor.doctor_appointment.filter(name=p_name, notes=p_notes)


            if  (this!= None and p_name == str(this.name) and p_notes == str(this.notes)):
                pass
            elif (len(patient_prescriptions) > 0):
                self._errors['name'] = ["Patient already this prescription"]
                return False
            return True
        except Exception as e:
            print(e)
            return True


class ViewPrescriptionsForm(forms.Form):
    """
    A list of patient's prescriptions
    """
    """
    def __init__(self, *args, **kwargs):

        user = kwargs.pop('user')
        super(ViewPrescriptionsForm, self).__init__(*args, **kwargs)
        if(user.first_name=='patient'):
            self.prescriptions = user.patient_prescriptions.all()
            prescriptions_partner = 'doctor' # patient is partnered with a doctor and vice versa
        else:
            self.prescriptions = user.doctor_prescriptions.all()
            prescriptions_partner = 'patient'
        choices = []

        for i, prescriptions in enumerate(self.presceiptions):
            partner_first_name = prescriptions.associated_patient.patient_user_profile.first_name if (prescriptions_partner=='patient') else prescriptions.associated_doctor.doctor_user_profile.first_name
            partner_last_name = prescriptions.associated_patient.patient_user_profile.last_name if (prescriptions_partner=='patient') else prescriptions.associated_doctor.doctor_user_profile.last_name
            choices.append((prescriptions, 'Prescription: {}, {}, with {} {}'
                            .format(prescriptions.name, prescriptions.notes, partner_first_name, partner_last_name)))

        self.fields['prescriptions'] = forms.ChoiceField(label="", choices=choices, widget=forms.RadioSelect)

    """
    def __init__(self, *args, **kwargs):
        patient = Patient.objects.get(user=kwargs.pop('patient'))
        super(ViewPrescriptionsForm, self).__init__(*args, **kwargs)
        prescriptions = Prescriptions.objects.filter(patient=patient)
        #self.fields['name', 'notes'] = forms.ChoiceField(label="", widget=forms.RadioSelect(), display=prescriptions)


class EditPrescriptionsForm(forms.ModelForm):
    """
    A doctor uses this form to edit or update a patient's prescriptions
    """
    class Meta:
        model = Prescriptions
        fields = ('name', 'notes')

    def __init__(self, *args, **kwargs):
        super(EditPrescriptionsForm, self).__init__(*args, **kwargs)


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
    Form for a user to read a specific message
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
    Form for a user to view all of their incoming messages
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
    Form for a user to create a private message
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
        """if (user.first_name == 'doctor'):
            profileInfo = user.doctor_user_profile
        elif (user.first_name == 'nurse'):
            profileInfo = user.nurse_user_profile
        elif (user.first_name == 'admin'):
            profileInfo = user.admin_user_profile
        else:
            profileInfo = user.patient_user_profile"""
        self.fields['sender_field'] = forms.CharField(initial='{}'.format(user), widget=forms.TextInput(attrs={'readonly':'readonly'}))
        self.fields['receiver_field'] = forms.ChoiceField(choices=choices, initial=receiver)
        self.fields['message_content'] = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 40, 'style': 'resize:none;'}))


class AddHospitalForm(forms.ModelForm):
    """
    Form for an administrator to add a hospital
    """

    class Meta:
        model = Hospital
        fields = ('name',)


class TransferPatientForm(forms.Form):
    """
    Form for an administrator to transfer a patient to a hospital
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
    Form for a doctor or nurse to admit a discharged patient to his hospital
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
    """
    Form for a nurse or a doctor to edit a patient's medical info
    """
    heart_rate = forms.CharField(required=False)
    diastolic_blood_pressure = forms.CharField(required=False)
    systolic_blood_pressure = forms.CharField(required=False)

    class Meta:
        model = MedicalInfo
        fields = ('height', 'weight', 'heart_rate', 'diastolic_blood_pressure', 'systolic_blood_pressure')


class DischargePatientForm(forms.Form):
    """
    Form for a doctor to discharge a patient in the doctor's hospital from that hospital
    """

    def __init__(self, *args, **kwargs):
        user = User.objects.get(username=kwargs.pop('user'))
        super(DischargePatientForm, self).__init__(*args, **kwargs)
        hospitals = user.hospital_set.all()
        patients = []
        for i, hospital in enumerate(hospitals):
            patient_list = hospital.people.filter(first_name='patient')
            for j, patient in enumerate(patient_list):
                if(patient.patient_user_profile.current_hospital == hospital):
                    patients.append(patient)
        choices = []
        for i, patient in enumerate(patients):
            profileInfo = patient.patient_user_profile
            choices.append(
                (patient, '{} {}, Username: {}'.format(profileInfo.first_name, profileInfo.last_name, patient)))
        self.fields['patient'] = forms.ChoiceField(choices=choices)


class ViewTestsForm(forms.Form):
    """
    A list of tests that a patient has is presented as TYPE_CHOICES in this form
    """
    TYPE_CHOICES = make_choice_list('catalog/data/test_types.txt')

    def __init__(self, *args, **kwargs):
        patient = User.objects.get(username=kwargs.pop('patient'))
        super(ViewTestsForm, self).__init__(*args, **kwargs)
        tests = patient.tests.all()
        choices = []
        for i, test in enumerate(tests):
            type = test.type
            name = [item[1] for item in self.TYPE_CHOICES if item[0] == type]
            choices.append((test, 'Type: {}'.format(name[0])))
        self.fields['test'] = forms.ChoiceField(label="", choices=choices, widget=forms.RadioSelect())


class ReadTestForm(forms.ModelForm):
    """
    A patient that has selected a test can view information about that test
    The results and comments are hidden if the test is not yet released
    """

    TYPE_CHOICES = make_choice_list('catalog/data/test_types.txt')

    class Meta:
        model = Test
        fields = ('type', 'doctor', 'results', 'comments', 'released')

    def __init__(self, *args, **kwargs):

        super(ReadTestForm, self).__init__(*args, **kwargs)
        released = self.instance.released
        type = self.instance.type
        name = [item[1] for item in self.TYPE_CHOICES if item[0] == type]
        self.fields['type'].widget.attrs['readonly'] = True
        self.initial['type'] = name[0]
        self.fields['doctor'].widget.attrs['readonly'] = True
        self.fields['results'].widget.attrs['readonly'] = True
        self.fields['comments'].widget.attrs['readonly'] = True
        self.fields['released'] = forms.CharField()
        self.fields['released'].widget.attrs['readonly'] = True
        if (released == False):
            self.fields['results'].widget = forms.HiddenInput()
            self.fields['comments'].widget = forms.HiddenInput()


class EditTestForm(forms.ModelForm):
    """
    A doctor uses this form to edit or update a patient's tests using the choices presented in the test_types.txt document
    """
    TYPE_CHOICES = make_choice_list('catalog/data/test_types.txt')
    class Meta:
        model = Test
        fields = ('type', 'results', 'comments', 'released')

    def __init__(self, *args, **kwargs):
        super(EditTestForm, self).__init__(*args, **kwargs)

        self.fields['type'] = forms.ChoiceField(choices=self.TYPE_CHOICES)
        self.fields['released'] = forms.BooleanField(required=False)


class ViewLogForm(forms.ModelForm):
    """
    #Form for a user to view the system log
    """

    class Meta:
        model = LogEntry
        fields = ('user', 'message', 'time')

    def __init__(self, *args, **kwargs):
        super(ViewLogForm, self).__init__(*args, **kwargs)
        self.fields['user'] = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
        self.fields['message'] = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
        self.fields['time'] = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly', 'rows': 1, 'cols': 40, 'style': 'resize:none;'}))

class ViewStatisticsForm(forms.Form):
    """
    Form for an admit to view hospital statistics
    """
    def __init__(self, *args, **kwargs):
        user = User.objects.get(username=kwargs.pop('user'))
        choice = int(kwargs.pop('choice'))

        super(ViewStatisticsForm, self).__init__(*args, **kwargs)
        hospitals = Hospital.objects.all()
        hospital = None
        choices = []
        for i, hosp in enumerate(hospitals):
            if (i == choice):
                hospital = hosp
            choices.append((i, hosp))
        self.fields['hospital'] = forms.ChoiceField(choices=choices, widget=forms.Select(attrs={"onChange":'submit()'}))
        self.initial['hospital'] = choice
        stats = SysStats.objects.get(hospital=hospital)
        sum = timezone.now()
        sum -= timezone.now()
        num = 0
        if stats.admissions.all() != None:
            for i, admission in enumerate(stats.admissions.all()):
                print((admission.discharge_time - admission.admission_time))
                sum += (admission.discharge_time - admission.admission_time)
                num += 1

            if (num == 0):
                num = 1
            average_stay = (sum/num)
            average_stay = average_stay - datetime.timedelta(microseconds=average_stay.microseconds)
        else:
            average_stay = 0
        self.fields['average_stay'] = forms.CharField(initial = average_stay, widget=forms.TextInput(attrs={'readonly':'readonly', 'value':'5'}))
        self.fields['patient_count'] = forms.CharField(initial=stats.patient_count,
                                                      widget=forms.TextInput(attrs={'readonly': 'readonly'}))
        self.fields['doctor_count'] = forms.CharField(initial=stats.doctor_count,
                                                      widget=forms.TextInput(attrs={'readonly': 'readonly'}))
        self.fields['nurse_count'] = forms.CharField(initial=stats.nurse_count,
                                                      widget=forms.TextInput(attrs={'readonly': 'readonly'}))
        self.fields['admin_count'] = forms.CharField(initial=stats.admin_count,
                                                     widget=forms.TextInput(attrs={'readonly': 'readonly'}))
