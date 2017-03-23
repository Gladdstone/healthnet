from django.shortcuts import render, redirect
from django.views import generic
from .forms import CreateAppointmentForm, ChooseAppointmentForm
from django import forms
from django.contrib.auth.models import User
from .models import Appointment
from django.forms.formsets import formset_factory






class Appointment(generic.ListView):
    def create(request):
        """
        Create an appointment and add it to the database
        :return: redirects user to the create appointment template or to home
        """
        #print('create')
        if request.method == "POST":
            #Appointment.objects.all().delete()
            #print(request.POST)
            if "cancel" in request.POST:
                return redirect('home')
            form = CreateAppointmentForm(request.POST)
            #print(title_exists(request.user, request.POST.get('title')))
            if form.is_valid(user=request.user, title=request.POST.get('title'), date_year=request.POST.get('date_year'),
                             date_month=request.POST.get('date_month'), date_day=request.POST.get('date_day'), time=request.POST.get('time'), this = None):# and not title_exists(request.user, request.POST.get('title')):
                post = form.save(commit=False)
                post.month = post.date.month
                post.year = post.date.year
                post.day = post.date.day
                post.save()
                patient = request.user.patient_user_profile
                try:
                    #checking if emergency contact info matches with patient in database
                        request.user.patient_appointment.add(post)
                        request.user.save()
                        post.save()
                    #message = 'Emergency contact linked to existing patient'
                except Exception as err:
                    print("Exception {0}".format(err))
                    #message = 'Emergency contact not linked to any existing patient'

                return render(request, 'return_home_message.html', {'message': 'Appointment created', 'url': 'index'})
        else:
            #print(request.method)
            form = CreateAppointmentForm()
        return render(request, '../templates/appointments/create_appointment.html', {'form': form})

    def update(request, title, **kwargs):
        """
        Update a specific appointment to a user in the database. The database removes and re-adds the appointment if it is updated because that was how I could get it to work
        :param appointment: appointment title to update
        :return: redirects user to template to either go home when completed or prompt for appointment updating
        """

        try:
            username = kwargs.pop('username')
            user = User.get(username=username)
            if(user.first_name == 'doctor'):
                appointment = user.doctor_appointment.get(title=title)
            else:
                appointment = user.patient_appointment.get(title=title)
        except Exception:
            appointment = request.user.patient_appointment.get(title=title)



        if request.method == "POST":
            #print('updating')
            # Appointment.objects.all().delete()
            if "cancel" in request.POST:
                return redirect('home')
            form = CreateAppointmentForm(request.POST)
            #temp = request.user.patient_appointment.filter(title=appointment)
            #request.user.patient_appointment.filter(title=appointment).delete()
            if form.is_valid(user=request.user, title=request.POST.get('title'),
                             date_year=request.POST.get('date_year'),
                             date_month=request.POST.get('date_month'), date_day=request.POST.get('date_day'),
                             time=request.POST.get('time'), this = appointment):  # and not title_exists(request.user, request.POST.get('title')):
                post = form.save(commit=False)
                post.month = post.date.month
                post.year = post.date.year
                post.day = post.date.day
                post.save()
                appointment.delete()
                try:
                    request.user.patient_appointment.add(post)
                    request.user.save()
                    post.save()
                except Exception as err:
                    print("Exception {0}".format(err))

                return redirect('index')  # , pk=post.pk)
        else:
            form = CreateAppointmentForm(instance=appointment)
        return render(request, '../templates/appointments/create_appointment.html', {'form': form})

    def view(request, **kwargs):  # , appointments_date):
        """
        View the appointments. Gives option to update or delete as well
        :return: renders a request to redirect user to viewing appointment template
        """

        try:
            username = kwargs.pop('username')
            user = User.get(username=username)
            if(user.first_name == 'doctor'):
                appointment_list = user.doctor_appointment
            else:
                appointment_list = user.patient_appointment
        except Exception:
            appointment_list = request.user.patient_appointment


        if request.method == 'POST':
            if 'delete' in request.POST:
                form = ChooseAppointmentForm(request.POST, user=request.user)
                if form.is_valid():
                    appointment_list.filter(title=request.POST.get('appointments')).delete()
                form = ChooseAppointmentForm(user=request.user)
            else:
                print(request.user.patient_user_profile)
                form = ChooseAppointmentForm(request.POST, user=request.user)
                if form.is_valid():
                    appointment = appointment_list.get(title=request.POST.get('appointments'))
                    request.method = 'GET'
                    return redirect('update_appointment', appointment)
        else:
            form = ChooseAppointmentForm(user=request.user)
            try:
                a = appointment_list.all()  # pk=appointments_date)
            except Exception as e:
                print(e)
                a = None
        return render(request, 'appointments/appointment.html', {'form': form})



class Home(generic.ListView):
    """
    Direct to the home page
    """
    template_name = 'base_generic.html'

    def index(request):
        return render(
            request,
            'index.html',
        )

def title_exists(user, title):
    """

    :param user: the user the appointment is associated with
    :param title: the title of the appointment
    :return: if the user has an appointment with the specific title
    """
    try:
        i = user.patient_appointment.filter(title=title)
        if(len(i)>0):
            return True
        return False
    except Exception as e:
        return False