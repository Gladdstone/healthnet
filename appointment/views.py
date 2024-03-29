from django.http import Http404
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

        if (not request.user.is_authenticated()):
            raise Http404
        if (request.user.first_name == 'nurse'):
            user = request.user.nurse_user_profile.current_doctor
        else:
            user = request.user



        if request.method == "POST":
            #Appointment.objects.all().delete()
            #print(request.POST)
            if "cancel" in request.POST:
                return redirect('index')
            form = CreateAppointmentForm(request.POST, hospital=user.hospital_set.all(), user=user) # ***PLACEHOLDER***
            if (user.first_name == 'doctor'):
                doctor = user
                patient = request.POST.get('patient')
            else:
                doctor = request.POST.get('doctor')
                patient = user
            #doctor = request.POST.get('doctor')
            #patient = request.POST.get('patient')

            if form.is_valid(doctor=doctor, patient=patient, date_year=request.POST.get('date_year'),
                             date_month=request.POST.get('date_month'), date_day=request.POST.get('date_day'), time=request.POST.get('time'), this = None):
                post = form.save(commit=False)
                if(user.first_name == 'doctor'):
                    patient = User.objects.get(username=request.POST.get('patient'))
                    doctor = user

                else:
                    doctor = User.objects.get(username=request.POST.get('doctor'))
                    patient = user


                post.month = post.date.month
                post.year = post.date.year
                post.day = post.date.day
                post.save()
                doctor.doctor_appointment.add(post)
                patient.patient_appointment.add(post)
                patient.save()
                doctor.save()
                #patient = request.user.patient_user_profile
                """try:
                    #checking if emergency contact info matches with patient in database
                        request.user.patient_appointment.add(post)
                        request.user.save()
                        post.save()
                    #message = 'Emergency contact linked to existing patient'
                except Exception as err:
                    print("Exception {0}".format(err))
                    #message = 'Emergency contact not linked to any existing patient'"""

                return render(request, 'return_home_message.html', {'message': 'Appointment created', 'url': 'index'})
        else:
            form = CreateAppointmentForm(hospital=user.hospital_set.all(), user=user) # ***PLACEHOLDER***
        return render(request, 'form_generic.html', {'form': form, 'title': 'Create Appointment'})

    def update(request, id, username):
        """
        Update a specific appointment to a user in the database. The database removes and re-adds the appointment if it is updated because that was how I could get it to work
        :param id: appointment to update
        :param username: username of user whose appointment is getting updated
        :return: redirects user to template to either go home when completed or prompt for appointment updating
        """

        if (not request.user.is_authenticated()):
            raise Http404
        user = User.objects.get(username=username)
        if(user.first_name == 'doctor'):
            appointment = user.doctor_appointment.get(id=id)
        else:
            appointment = user.patient_appointment.get(id=id)



        if request.method == "POST":
            #print('updating')
            # Appointment.objects.all().delete()
            if "cancel" in request.POST:
                return redirect('index')
            form = CreateAppointmentForm(request.POST, hospital=user.hospital_set.all(), user=user) # ***PLACEHOLDER***
            doctor = request.POST.get('doctor')
            print(doctor)
            patient = request.POST.get('patient')
            if form.is_valid(doctor=doctor, patient=patient,
                             date_year=request.POST.get('date_year'),
                             date_month=request.POST.get('date_month'), date_day=request.POST.get('date_day'),
                             time=request.POST.get('time'), this = appointment):
                post = form.save(commit=False)

                if (user.first_name == 'doctor'):
                    patient = User.objects.get(username=request.POST.get('patient'))
                    doctor = user
                else:
                    doctor = User.objects.get(username=request.POST.get('doctor'))
                    patient = user

                post.month = post.date.month
                post.year = post.date.year
                post.day = post.date.day
                post.save()
                appointment.delete()
                doctor.doctor_appointment.add(post)
                patient.patient_appointment.add(post)
                patient.save()
                doctor.save()

                return redirect('index')  # , pk=post.pk)
        else:
            form = CreateAppointmentForm(instance=appointment, hospital=user.hospital_set.all(), user=user) # ***PLACEHOLDER***
            return render(request, 'form_generic.html', {'form': form, 'title': 'Update Appointment'})

    def view(request, **kwargs):  # , appointments_date):
        """
        View the appointments. Gives option to update or delete as well
        :return: renders a request to redirect user to viewing appointment template
        """
        if (not request.user.is_authenticated()):
            raise Http404
        if(request.user.first_name == 'nurse'):
            user = request.user.nurse_user_profile.current_doctor
            if user == None:
                return redirect('select_doctor')
        else:
            user = request.user

        if(user.first_name == 'doctor'):
            appointment_list = user.doctor_appointment
            name = "{} {}".format(user.doctor_user_profile.first_name, user.doctor_user_profile.last_name)
        else:
            appointment_list = user.patient_appointment
            name = "{} {}".format(user.patient_user_profile.first_name, user.patient_user_profile.last_name)



        if request.method == 'POST':
            if 'back' in request.POST:
                return redirect('index')
            if 'delete' in request.POST:
                form = ChooseAppointmentForm(request.POST, user=user)
                if form.is_valid():
                    appointment_list.filter(id=request.POST.get('appointments')).delete()
                form = ChooseAppointmentForm(user=user)
            elif 'create' in request.POST:
                return redirect('create_appointment')
            else:
                #print(request.user.patient_user_profile)
                form = ChooseAppointmentForm(request.POST, user=user)
                if form.is_valid():
                    appointment = appointment_list.get(id=request.POST.get('appointments'))
                    request.method = 'GET'
                    return redirect('update_appointment', appointment, user)
        else:
            form = ChooseAppointmentForm(user=user)
            try:
                a = appointment_list.all()  # pk=appointments_date)
            except Exception as e:
                print(e)
                a = None
        return render(request, 'appointments/appointment.html', {'form': form, 'name': name, 'user':request.user}) # in this case, user is the literal user of the program who is logged in

