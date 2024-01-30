#_app/views.py
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

TARGET_DIR = 'account/'

def signupfunc(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            User.objects.create_user(username, '', password)
            return render(request, 'account/login.html', {})
        except IntegrityError:
            return render(request, 'account/signup.html', {'error': 'このユーザはすでに登録されています'})

    return render(request, TARGET_DIR+'signup.html', {})

def loginfunc(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        
        else:
            return render(request, 'account/login.html', {})
    
    return render(request, TARGET_DIR+'login.html', {})