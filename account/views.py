#_app/views.py
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render


def loginfunc(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        
        else:
            return render(request, 'account/login.html', {'error': 'ユーザー名かパスワードが正しくありません'})
    
    return render(request, 'account/login.html', {})