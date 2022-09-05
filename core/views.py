from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import *
from django.http import HttpResponse


# Create your views here.

def index(request):
    return render(request, 'index.html')


def signup(request):

    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password == password2:

            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email is already taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'User is already Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()

                return redirect('signin')

        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')

    else:
        return render(request, 'signup.html')


def signin(request):

    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')

        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')

    else:
        return render(request, 'signin.html')
