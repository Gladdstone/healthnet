from django.db import models

class Patient(models.Model):

    # Fields
    fname = models.CharField(max_length = 20, help_text = 'First name')
    lname = models.CharField(max_length = 20, help_text = 'Last name')
    email = models.EmailField(help_text = 'Email')
    dob = models.DateField(help_text = 'Date of Birth')
    ssn = models.CharField(max_length = 9, help_text = 'Social Security Number')
    address = models.TextField(max_length = 40, help_text = 'Address')
    city = models.CharField(max_length = 20, help_text = 'City')
    zip = models.CharField(max_length = 5, help_text = 'Zip Code')

    # Metadata
    class Meta:
        ordering = ['lname', '-dob', 'ssn']

    # Methods
    def __str__(self):
        return self.lname

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