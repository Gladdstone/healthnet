from django import forms

from .models import Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('username', 'password', 'first_name', 'last_name', 'email', 'phone_number', 'insurance', 'pref_hospital', 'emergency_contact', 'medical_info')