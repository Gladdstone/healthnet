from django.shortcuts import render, redirect
from django.views import generic
from .forms import CreateAppointmentForm, ChooseAppointmentForm
from django import forms
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






class Appointment(generic.ListView):
    def create(request):
        print('create')
        if request.method == "POST":
            #Appointment.objects.all().delete()
            print(request.POST)
            if "cancel" in request.POST:
                return redirect('home')
            form = CreateAppointmentForm(request.POST)
            print(title_exists(request.user, request.POST.get('title')))
            if form.is_valid(user=request.user, title=request.POST.get('title'), date_year=request.POST.get('date_year'),
                             date_month=request.POST.get('date_month'), date_day=request.POST.get('date_day'), time=request.POST.get('time')):# and not title_exists(request.user, request.POST.get('title')):
                post = form.save(commit=False)
                post.month = post.date.month
                post.year = post.date.year
                post.day = post.date.day
                post.save()
                patient = request.user.user_profile
                try:
                    #checking if emergency contact info matches with patient in database
                        request.user.patient.add(post)
                        request.user.save()
                        post.save()
                    #message = 'Emergency contact linked to existing patient'
                except Exception as err:
                    print("Exception {0}".format(err))
                    #message = 'Emergency contact not linked to any existing patient'

                return render(request, 'return_home_message.html', {'message': 'Appointment created', 'url': 'index'})
        else:
            print(request.method)
            form = CreateAppointmentForm()
        return render(request, '../templates/appointments/create_appointment.html', {'form': form})

    def update(request, appointment):
        if request.method == "POST":
            print('updating')
            # Appointment.objects.all().delete()
            if "cancel" in request.POST:
                return redirect('home')
            form = CreateAppointmentForm(request.POST)
            print('updating')
            request.user.patient.filter(title=appointment).delete()
            if form.is_valid(user=request.user, title=request.POST.get('title'),
                             date_year=request.POST.get('date_year'),
                             date_month=request.POST.get('date_month'), date_day=request.POST.get('date_day'),
                             time=request.POST.get(
                                 'time')):  # and not title_exists(request.user, request.POST.get('title')):
                post = form.save(commit=False)
                post.month = post.date.month
                post.year = post.date.year
                post.day = post.date.day

                post.save()
                try:
                    request.user.patient.add(post)
                    request.user.save()
                    post.save()
                    # message = 'Emergency contact linked to existing patient'
                except Exception as err:
                    print("Exception {0}".format(err))
                    # message = 'Emergency contact not linked to any existing patient'"""

                return redirect('index')  # , pk=post.pk)
        else:
            print('get')
            print(appointment)
            form = CreateAppointmentForm(instance=request.user.patient.get(title=appointment))
        return render(request, '../templates/appointments/create_appointment.html', {'form': form})

    def view(request):  # , appointments_date):

        if request.method == 'POST':
            if 'delete' in request.POST:
                form = ChooseAppointmentForm(request.POST, user=request.user)
                if form.is_valid():
                    request.user.patient.filter(title=request.POST.get('appointments')).delete()
                form = ChooseAppointmentForm(user=request.user)
            else:
                form = ChooseAppointmentForm(request.POST, user=request.user)
                if form.is_valid():
                    appointment = request.user.patient.get(title=request.POST.get('appointments'))
                    request.method = 'GET'
                    return redirect('update_appointment', appointment)
        else:
            form = ChooseAppointmentForm(user=request.user)
            try:
                a = request.user.patient.all()  # pk=appointments_date)
            except Exception as e:
                print(e)
                a = None
        return render(request, 'appointments/appointment.html', {'form': form})



class Home(generic.ListView):
    template_name = 'base_generic.html'

    def index(request):
        return render(
            request,
            'index.html',
        )

def title_exists(user, title):
    try:
        i = user.patient.filter(title=title)
        if(len(i)>0):
            return True
        return False
    except Exception as e:
        return False