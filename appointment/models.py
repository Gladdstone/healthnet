from django.db import models
from django.utils import timezone


class Appointment(models.Model):
    date = models.DateTimeField('appointment date')
    doctor = models.CharField(max_length=20) #Dr. Smith

    def __str__(self):
        return self.title