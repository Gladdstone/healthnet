from django.shortcuts import render, redirect
from django.views import generic
from .forms import CreateAppointmentForm
from django.contrib.auth.models import User
from .models import Appointment
from django.forms.formsets import formset_factory
"""
class CreateAppointment(generic.ListView):
    template_name = 'registration/patient_registration.html'

    def create(request):
        if request.method == "POST":
            if "cancel" in request.POST:
                return redirect('index')
            form = CreateAppointment(request.POST)
            if form.is_valid():
                apptInfo = form.save(commit=False)
                apptInfo.save()
				
                return redirect('index')
        else:
            form = CreateAppointment()
        return render(request, '../templates/create_appointment.html', {'form': form})
"""


def appointments(request):#, appointments_date):
    try:
        a = Appointment.objects.filter()#pk=appointments_date)
    except Exception as e:
        a = None
    return render(request, 'appointments/appointment.html', {'appointments': a})


class CreateAppointment(generic.ListView):
    def create(request):
        if request.method == "POST":
            if "cancel" in request.POST:
                return redirect('home')
            form = CreateAppointmentForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.save()
                return redirect('index')#, pk=post.pk)
        else:
            print(request.method)
            form = CreateAppointmentForm()
        return render(request, '../templates/appointments/create_appointment.html', {'form': form})


class Home(generic.ListView):
    template_name = 'base_generic.html'

    def index(request):
        return render(
            request,
            'index.html',
        )
