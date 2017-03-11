from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.forms import widgets


class PatientProfileInfo(models.Model):

    # Fields
    user = models.OneToOneField(User, unique=True, related_name="user_profile")
    #username = models.CharField(max_length=200, default="")
    #password = models.CharField(max_length=200, default="")
    first_name = models.CharField(max_length=200, default="")
    last_name = models.CharField(max_length=200, default="")
    #email = models.CharField(max_length=200, default="")

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], blank=True, max_length=16)
    insurance = models.CharField(max_length=200, default="")
    pref_hospital = models.CharField(max_length=200, default="")
    emergency_contact_first_name = models.CharField(max_length=200, default="")
    emergency_contact_last_name = models.CharField(max_length=200, default="")
    email_regex = RegexValidator(regex=r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
                                 message="Email must be entered in the format: 'xxxx@yyyy.zzz'.")
    emergency_contact_email = models.CharField(max_length=200, default="", validators=[email_regex])
    emergency_contact = models.ForeignKey(User, unique=False, null=True, blank=True)
    medical_info = models.CharField(max_length=200, default="")


    # Metadata
    class Meta:
        ordering = ['last_name']#, '-dob', 'ssn']

    # Methods
    def __str__(self):
        return self.last_name

class PatientRegisterInfo(models.Model):
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

    # Fields
    fname = models.CharField(max_length=20, help_text='First name')
    lname = models.CharField(max_length=20, help_text='Last name')
    email = models.EmailField(help_text='Email')
    dob = models.DateField(help_text='Date of Birth')

    # Metadata
    class Meta:
        ordering = ['lname', '-dob']

    # Methods
    def __str__(self):
        return self.lname

class Nurse(models.Model):

    # Fields
    fname = models.CharField(max_length=20, help_text='First name')
    lname = models.CharField(max_length=20, help_text='Last name')
    email = models.EmailField(help_text='Email')
    dob = models.DateField(help_text='Date of Birth')

    # Metadata
    class Meta:
        ordering = ['lname', '-dob']

    # Methods
    def __str__(self):
        return self.lname