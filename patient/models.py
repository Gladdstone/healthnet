from django.db import models
from django.utils import timezone


class Post(models.Model):
    #author = models.ForeignKey('auth.User')
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    insurance = models.CharField(max_length=200)
    pref_hospital = models.CharField(max_length=200)
    emergency_contact = models.CharField(max_length=200)
    medical_info = models.CharField(max_length=200)
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
