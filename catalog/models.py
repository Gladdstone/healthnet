from django.db import models
from django.contrib.auth.models import User

class PatientProfileInfo(models.Model):

    # Fields
    user = models.OneToOneField(User, unique=True)
    #username = models.CharField(max_length=200, default="")
    #password = models.CharField(max_length=200, default="")
    first_name = models.CharField(max_length=200, default="")
    last_name = models.CharField(max_length=200, default="")
    #email = models.CharField(max_length=200, default="")
    phone_number = models.CharField(max_length=200, default="")
    insurance = models.CharField(max_length=200, default="")
    pref_hospital = models.CharField(max_length=200, default="")
    emergency_contact = models.CharField(max_length=200, default="")
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
    email = models.CharField(max_length=200, default="")

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