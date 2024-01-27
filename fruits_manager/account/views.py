from django.shortcuts import render
from .forms import SignupForm, LoginForm
from django.contrib.auth import login


def signup_view(request):
    path = 'signup.html'

    if request.method == 'POST':

        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()

    else:
        form = SignupForm()
    
    param = {
        'form': form
    }
    return render(request, path, param)

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()

            if user:
                login(request, user)

    else:
        form = LoginForm()

    param = {
        'form': form,
    }

    return render(request, 'login.html', param)

def logout_view(request):
    pass

def user_view(request):
    user = request.user

    params = {
        'user': user
    }

    return render(request, 'top.html', params)

def other_view(request):
    pass