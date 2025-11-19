from django.shortcuts import render,redirect
from dataentry.tasks import celery_task
from django.http import HttpResponse
from .forms import RegistrationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login,logout



# Create your views here.
def home_page(request):
    return render(request, "home.html")

def celery_task_test(request):
    celery_task.delay()
    return HttpResponse('<h3>Task Completed Successfully</h3>')

def register(request):
    if request.method == 'POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Form is successfully submited")
            return redirect("register")
        else:
            context={'form':form}
            return render(request,"register.html",context)
    else:
        form=RegistrationForm()
        context={'form':form}
    return render(request,"register.html",context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect("home")
            else:
                messages.error(request, "Invalid credentials.")
        else:
            messages.error(request, "Invalid credentials.")
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect('login')