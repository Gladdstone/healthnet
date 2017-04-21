from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import User
from django import forms


class Appointment(models.Model):
	"""
	An appointment class that can be created by patients, doctors and nurses

	title: the title of the appointment
	date: the date that the appointment will take place
	time: the time of the appointment
	year: the appointment year
	day: the appointment day
	month: the appointment month
	doctor: the doctor field that a patient specifies
	patient: the patient field that a doctor specifies
	description: a description of the appointment and/or any symptoms that the patient has
	associated_patient: the patient that is associated with this appointment
	associated_doctor: the doctor that is associated with this appointment
	"""
	title = models.CharField(max_length=200)
	date = models.DateField(default=datetime.date(2000, 1, 1))
	time = models.TimeField(default=datetime.time)
	year = models.IntegerField()
	day = models.IntegerField()
	month = models.IntegerField()
	doctor = models.CharField(max_length=200) #placeholder
	patient = models.CharField(max_length=200)
	description = models.CharField(max_length=200, blank=True, null=True)
	associated_patient = models.ForeignKey(User, unique=False, null=True, blank=True, related_name='patient_appointment')
	associated_doctor = models.ForeignKey(User, unique=False, null=True, blank=True, related_name='doctor_appointment')

	def __str__(self):
		return str(self.id)
