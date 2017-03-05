from django.db import models
from django.utils import timezone


class Appointments(models.Model):
    date = models.CharField(max_length=10) #03/18/2017
    time = models.CharField(max_length=8, default=timezone.now()) #11:20:26

    def __str__(self):
        return self.date
