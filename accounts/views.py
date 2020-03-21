from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

# Create your views here.

def signup(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['confirm_password']:
            try:
                user  = User.objects.get(username=request.POST['username'])
                error = 'Username has already been taken. Please choose another one and try again'
                return render(request, 'accounts/signup.html', {"error":error})
            except User.DoesNotExist:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
                auth.login(request, user)
                return redirect('home')
        else:
                error = 'The Passwords do not match. Please try again'
                return render(request, 'accounts/signup.html', {"error":error})
    else:
        return render(request, 'accounts/signup.html', )

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            error = 'Username or Password is not correct. Please try again'
            return render(request, 'accounts/login.html', {'error':error})
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
    return render(request, 'products/home.html')
