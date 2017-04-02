import uuid

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.forms import widgets
import datetime


class Hospital(models.Model):
    """
    Class to represent hospitals
    """
    name = models.CharField(max_length=200, default="")
    people = models.ManyToManyField(User)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class MedicalInfo(models.Model):
    """
    Medical information that is linked to a patient
    """

    height = models.CharField(max_length=200, help_text='inches')
    weight = models.CharField(max_length=200, help_text='lbs')
    eye_color = models.CharField(max_length=200)
    birthday = models.DateField(default=datetime.date(2000, 1, 1))
    race = models.CharField(max_length=200)
    sex = models.CharField(max_length=200)
    diastolic_blood_pressure = models.IntegerField(blank=True, null=True, help_text='mmHg')
    systolic_blood_pressure = models.IntegerField(blank=True, null=True, help_text='mmHg')
    heart_rate = models.IntegerField(blank=True, null=True, help_text='BPM')

    # Metadata
    class Meta:
        ordering = ['birthday']  # , '-dob', 'ssn']

    # Methods
    def __str__(self):
        return self.birthday
        # return self.first_name + self.last_name

class Patient(models.Model):

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
    """

    sender = models.ForeignKey(User, on_delete=models.CASCADE, unique=False, null=True, blank=True, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, unique=False, null=True, blank=True, related_name="receiver")
    receiver_field = models.CharField(max_length=200)
    sender_field = models.CharField(max_length=200)
    message_content = models.CharField(max_length=200)
    created_at = models.TimeField(default=datetime.time)
    identifier = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)


    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.identifier


class LogEntry(models.Model):
    """
    Class to contain activity log queue
    """

    user = models.CharField(max_length=200)
    message = models.CharField(max_length=200)
    time = models.DateTimeField(default=datetime.datetime.now())

    class Meta:
        ordering = ['time']

    def __str__(self):
        return self.message
