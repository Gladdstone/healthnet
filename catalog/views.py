from django.shortcuts import render, redirect
from django.views import generic
from .forms import PatientRegisterProfileForm, PatientRegisterUserForm
from django.contrib.auth.models import User
from .models import PatientProfileInfo
from django.forms.formsets import formset_factory

# Create your views here.

def index(request):
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

                user = User.objects.create_user(username = request.POST.get("username"), password = request.POST.get("password"), email = request.POST.get('email'))
                profileInfo = form2.save(commit=False)
                profileInfo.user = user
                profileInfo.save();
                #patient = PatientProfileInfo(user=user);
                temp = User.objects.get(username='ayylmao')
                print(temp.patientprofileinfo.first_name)
                #print(User.objects.get(username='supbabe'))
                return redirect('index')
        else:
            form = PatientRegisterUserForm()
            form2 = PatientRegisterProfileForm();
        return render(request, '../templates/registration/patient_registration.html', {'form': form, 'form2': form2})