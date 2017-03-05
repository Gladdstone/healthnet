from django.shortcuts import render, redirect
from django.views import generic
from .forms import PostForm

class PatientRegistration(generic.ListView):
    template_name = 'registration/patient_registration.html'

    def register(request):
        if request.method == "POST":
            if "cancel" in request.POST:
                return redirect('home')
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.save()
                return redirect('home', pk=post.pk)
        else:
            print(request.method)
            form = PostForm()
        return render(request, '../templates/registration/patient_registration.html', {'form': form})

class Home(generic.ListView):
    template_name = 'base_generic.html'

    def index(request):
        return render(
            request,
            'index.html',
        )

