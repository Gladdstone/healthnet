import uuid

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.forms import widgets
import datetime
from django.utils import timezone


class Hospital(models.Model):
    """
    Class to represent hospitals

    name: name of the hospital
    people: people that have been, or are currently in that hospital, either staff or patients
    """
    name = models.CharField(max_length=200, default="", unique=True)
    people = models.ManyToManyField(User)
    #admissions = 0
    #stay_lengths = []

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Prescriptions(models.Model):
    """
    Class to represent Prescriptions
    """
    name = models.CharField(max_length=200)
    notes = models.CharField(max_length=500, blank=True)
    patient = models.CharField(max_length=200, default="")
    associated_patient = models.ForeignKey(User, unique=False, null=True, blank=True,
                                           related_name='patient_prescription')
    associated_doctor = models.ForeignKey(User, unique=False, null=True, blank=True, related_name='doctor_prescription')
    associated_hospital = models.ForeignKey(User, unique=False, null=True, blank=True,
                                            related_name='hospital_prescriptions')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Test(models.Model):
    """
    Class that represents an individual test result that is linked to a patient

    type: type of test
    results: test results
    released: has the doctor released this test yet
    comments: comments on the test by the doctor
    patient: user foreign key that the test is for
    doctor: string to let a patient know who released the test
    """

    type = models.CharField(max_length=100)
    results = models.CharField(max_length=500)
    comments = models.CharField(max_length=200)
    released = models.BooleanField()
    patient = models.ForeignKey(User, on_delete=models.CASCADE, unique=False, null=True, blank=True, related_name='tests')
    doctor = models.CharField(max_length=50)

    class Meta:
        ordering = ['type', 'doctor']

    def __str__(self):
        return str(self.id)

class MedicalInfo(models.Model):
    """
    Medical information that is linked to a patient

    all fields are just values that can be input into the medical info
    """
    #patient/doctor/nurse entered
    height = models.CharField(max_length=200, help_text='inches')
    weight = models.CharField(max_length=200, help_text='lbs')
    #patient entered
    eye_color = models.CharField(max_length=200)
    birthday = models.DateField(default=datetime.date(2000, 1, 1))
    race = models.CharField(max_length=200)
    sex = models.CharField(max_length=200)
    #doctor/nurse entered
    diastolic_blood_pressure = models.IntegerField(blank=True, null=True, help_text='mmHg')
    systolic_blood_pressure = models.IntegerField(blank=True, null=True, help_text='mmHg')
    heart_rate = models.IntegerField(blank=True, null=True, help_text='BPM')

    # Metadata
    class Meta:
        ordering = ['birthday']  # , '-dob', 'ssn']

    # Methods
    def __str__(self):
        return str(self.id)
        # return self.first_name + self.last_name

class Patient(models.Model):
    """
    The profile info of a patient

    user: the associated user object to the patient
    first_name: a patient's first name
    last_name: a patient's last name
    phone_number: a patient's phone number
    insurance: a patient's proof of insurance
    pref_hospital: a patient's preferred hospital
    emergency_contact_first_name: first name of emergency contact
    emergency_contact_last_name: last name of emergency contact
    emergency_contact_email: email for the emergency contact
    emergency_contact: linked to an emergency contact if other details match a patient in the system
    medical_info: a patient's medical info object
    current_hospital: the hospital that the patient is currently admitted to
    """

    # Fields
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, related_name="patient_user_profile") #links the patient's profile information to a user in the database
    first_name = models.CharField(max_length=200, default="")
    last_name = models.CharField(max_length=200, default="")

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], blank=False, max_length=16)
    insurance = models.CharField(max_length=200, default="")
    pref_hospital = models.CharField(max_length=200, default="")
    emergency_contact_first_name = models.CharField(max_length=200, default="")
    emergency_contact_last_name = models.CharField(max_length=200, default="")
    email_regex = RegexValidator(regex=r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
                                 message="Email must be entered in the format: 'xxxx@yyyy.zzz'.")
    emergency_contact_email = models.CharField(max_length=200, default="", validators=[email_regex])
    emergency_contact = models.ForeignKey(User, on_delete=models.CASCADE, unique=False, null=True, blank=True) #links a patient to an emergency contact in the database
    medical_info = models.OneToOneField(MedicalInfo, on_delete=models.CASCADE, unique=True, null=True)
    current_hospital = models.ForeignKey(Hospital, unique=False, null=True, blank=True)
    admission_time = models.DateTimeField(default=timezone.now)

    # Metadata
    class Meta:
        ordering = ['last_name']#, '-dob', 'ssn']

    # Methods
    def __str__(self):
        return self.user.username
        #return self.first_name + self.last_name

class UserInfo(models.Model):
    """
    This model is used for the literal django User registration
    """
    username = models.CharField(max_length=200, default="")
    password = models.CharField(max_length=200, default="")
    re_enter_password = models.CharField(max_length=200, default="")
    email_regex = RegexValidator(regex=r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
                                 message="Email must be entered in the format: 'xxxx@yyyy.zzz'.")
    email = models.CharField(max_length=200, default="", validators=[email_regex])

    # Metadata
    class Meta:
        ordering = ['username']  # , '-dob', 'ssn']

    # Methods
    def __str__(self):
        return self.username

class Doctor(models.Model):
    """
    Class for Doctor users

    user: user who is associated with this doctor object
    first_name: a doctor's first name
    last_name: a doctor's last name
    hospital: the hospital that a doctor works at when he is registered
    """
    # Fields
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, related_name="doctor_user_profile") #links the doctor's profile information to a user in the database
    first_name = models.CharField(max_length=200, default="")
    last_name = models.CharField(max_length=200, default="")
    hospital = models.CharField(max_length=200, default="")

    # Metadata
    class Meta:
        ordering = ['last_name']

    # Methods
    def __str__(self):
        return self.user.username

class Nurse(models.Model):
    """
    Class for Nurse users

    user: user who is associated with this nurse object
    first_name: a nurse's first name
    last_name: a nurse's last name
    current_doctor: a link to a doctor who is selected and the nurse can look at his appointments and the like
    hospital: the hospital that a nurse works at when he is registered
    """
    # Fields
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, related_name="nurse_user_profile") #links the nurse's profile information to a user in the database
    first_name = models.CharField(max_length=200, default="")
    last_name = models.CharField(max_length=200, default="")
    current_doctor = models.OneToOneField(User, unique=False, null=True, blank=True, related_name="current_doctor") #the currently selected doctor for viewing appointments, etc.
    hospital = models.CharField(max_length=200, default="")

    # Metadata
    class Meta:
        ordering = ['last_name']

    # Methods
    def __str__(self):
        return self.user.username

class Admin(models.Model):
    """
    Class for Admin users

    user: user who is associated with this admin object
    first_name: a admin's first name
    last_name: a admin's last name
    hospital: the hospital that an admin works at when he is registered
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, related_name="admin_user_profile") #links the admin's profile information to a user in the database
    first_name = models.CharField(max_length=200, default="")
    last_name = models.CharField(max_length=200, default="")
    hospital = models.CharField(max_length=200, default="")

    class Meta:
        ordering = ['last_name']

    # Methods
    def __str__(self):
        return self.user.username


class PrivateMessage(models.Model):
    """
    Class to represent and hold information for a message

    sender: user associated with sending this message
    receiver: user associated with receiving this message
    receiver_field: field that a user inputs the receiver when creating a message. This is then translated into the receiver
    receiver_field: field that is filled out as the sender when creating a message. This is then translated into the sender
    message_contact: the contact that is typed into a message
    created_at: time that the message was sent
    """

    sender = models.ForeignKey(User, on_delete=models.CASCADE, unique=False, null=True, blank=True, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, unique=False, null=True, blank=True, related_name="receiver")
    receiver_field = models.CharField(max_length=200)
    sender_field = models.CharField(max_length=200)
    message_content = models.CharField(max_length=200)
    created_at = models.TimeField(default=datetime.time)


    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return str(self.id)


class LogEntry(models.Model):
    """
    #Class to contain activity log queue
"""

    user = models.ForeignKey(User, unique=False, null=True, blank=True, on_delete=models.CASCADE, related_name='log_entry')
    message = models.CharField(max_length=200)
    time = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-time']

    def __str__(self):
        return str(self.id)



class SysStats(models.Model):
    """
    #Class to contain system statistics
    """

    hospital = models.OneToOneField(Hospital, on_delete=models.CASCADE, unique=True, null=True, blank=True, related_name="statistics")

    # general model counting
    patient_count = models.IntegerField(default=0)  #X
    doctor_count = models.IntegerField(default=0)   #X
    nurse_count = models.IntegerField(default=0)    #X
    admin_count = models.IntegerField(default=0)    #X



    # used for ordering and identification
    timestamp = models.DateField(default=timezone.now)

    def __str__(self):
        return str(self.hospital)

class AdmissionInfo(models.Model):
    """
    Class to represent information when a patient is admitted/discharged/transferred
    """
    admission_time = models.DateTimeField(default=timezone.now)
    discharge_time = models.DateTimeField(default=timezone.now)
    patient = models.ForeignKey(User, unique=False, null=True, blank=True, on_delete=models.CASCADE, related_name = 'admission_info')
    statistics = models.ForeignKey(SysStats, unique=False, null=True, blank=True, on_delete=models.CASCADE,
                                   related_name='admissions')

