from django.shortcuts import render, redirect
from django.views import generic
from .forms import *
from django.contrib.auth.models import User
from .models import PatientProfileInfo
from django.forms.formsets import formset_factory

# Create your views here.

def index(request):

    if request.user.is_authenticated() and request.user.first_name == 'patient':
        return render(
            request,
            'patient_home.html',
        )
    return render (
        request,
        'index.html',
    )

def index2(request):
    return render (
        request,
        'index2.html',
    )

class PatientRegistration(generic.ListView):
    template_name = 'registration/patient_registration.html'

    def register(request):
        if request.method == "POST":
            if "cancel" in request.POST:
                return redirect('index')
            form = PatientRegisterUserForm(request.POST)
            form2 = PatientRegisterProfileForm(request.POST);
            if all([form.is_valid(), form2.is_valid()]):
                userInfo = form.save(commit=False)
                userInfo.save()
                User.objects.all().delete()

                user = User.objects.create_user(username = request.POST.get("username"), password = request.POST.get("password"), email = request.POST.get('email'), first_name = 'patient')

                profileInfo = form2.save(commit=False)
                profileInfo.user = user
                profileInfo.save();
                #patient = PatientProfileInfo(user=user);
                #print(User.objects.get(username='supbabe'))
                return redirect('index')
        else:
            form = PatientRegisterUserForm()
            form2 = PatientRegisterProfileForm();
        return render(request, '../templates/registration/patient_registration.html', {'form': form, 'form2': form2})

class PatientProfile(generic.edit.CreateView):
    def view(request):
        if request.method == "POST":
            print(request.POST)
            if "update" in request.POST:
                return redirect('patient_profile_update')
        profileInfo = request.user.patientprofileinfo
        basicInfo = {'first_name': profileInfo.first_name, 'last_name': profileInfo.last_name,
                     'phone_number': profileInfo.phone_number}
        return render(request, 'patient_view_profile.html', {'basicInfo': basicInfo})

    def update_basic(request):
        """if request.method == 'POST':
            if "cancel" in request.POST:
                return redirect('patient_profile')
        form = PatientUpdateBasicInfoForm(request.user.patientprofileinfo)
        return render(request, 'patient_view_profile.html', {'form': form})"""


