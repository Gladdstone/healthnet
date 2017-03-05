from django import forms

from .models import Appointment


class PostForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = ('date', 'doctor')
