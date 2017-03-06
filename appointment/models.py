from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import User
from django import forms


class Appointment(models.Model):
	date = models.DateField(default=datetime.datetime.now)
	time = models.TimeField(default=datetime.time)
	doctor = models.CharField(max_length=200) #placeholder
	#doctor = models.OneToOneField(User)

	def __str__(self):
		return self.doctor