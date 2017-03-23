from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.forms import widgets


class Patient(models.Model):

    # Fields
    user = models.OneToOneField(User, unique=True, related_name="patient_user_profile") #links the patient's profile information to a user in the database
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
    emergency_contact = models.ForeignKey(User, unique=False, null=True, blank=True) #links a patient to an emergency contact in the database
    medical_info = models.CharField(max_length=200, default="")


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
    user = models.OneToOneField(User, unique=True, related_name="doctor_user_profile") #links the doctor's profile information to a user in the database
    first_name = models.CharField(max_length=200, default="")
    last_name = models.CharField(max_length=200, default="")

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
    user = models.OneToOneField(User, unique=True, related_name="nurse_user_profile") #links the nurse's profile information to a user in the database
    first_name = models.CharField(max_length=200, default="")
    last_name = models.CharField(max_length=200, default="")
    current_doctor = models.OneToOneField(User, unique=False, null=True, blank=True, related_name="current_doctor") #the currently selected doctor for viewing appointments, etc.

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

    user = models.OneToOneField(User, unique=True, related_name="admin_user_profile") #links the admin's profile information to a user in the database
    first_name = models.CharField(max_length=200, default="")
    last_name = models.CharField(max_length=200, default="")

    class Meta:
        ordering = ['last_name']

    # Methods
    def __str__(self):
        return self.user.username