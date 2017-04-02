from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import User
from django import forms


class Appointment(models.Model):
	title = models.CharField(max_length=200)
	date = models.DateField(default=datetime.date(2000, 1, 1))
	time = models.TimeField(default=datetime.time)
	year = models.IntegerField()
	day = models.IntegerField()
	month = models.IntegerField()
	doctor = models.CharField(max_length=200) #placeholder
	patient = models.CharField(max_length=200)
	associated_patient = models.ForeignKey(User, unique=False, null=True, blank=True, related_name='patient_appointment')
	associated_doctor = models.ForeignKey(User, unique=False, null=True, blank=True, related_name='doctor_appointment')

	def __str__(self):
		return self.title

class AppointmentSelect(models.Model):
	appt = models.CharField(max_length=200)

	def __str__(self):
		return self.appt