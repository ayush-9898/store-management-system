from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def index(req):

    if req.user.is_authenticated:
        return redirect('dashboard')

    if req.method == "POST":
        username = req.POST.get('username')
        password = req.POST.get('password')

        user = authenticate(req, username=username, password=password)

        if user is not None:
            login(req, user)
            return redirect('dashboard')
        else:
            return render(req, 'home/index.html', {
                'error': 'Invalid Username or Password'
            })

    return render(req, 'home/index.html')


@login_required
def dashboard(req):
    role = req.user.staff.role
    return render(req, 'home/dashboard.html', {'role': role})


def logout_view(req):
    logout(req)
    return redirect('home')