from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def index(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'home/index.html', {
                'error': 'Invalid Username or Password'
            })

    return render(request, 'home/index.html')


@login_required
def dashboard(request):
    role = request.user.staff.role
    return render(request, 'home/dashboard.html', {'role': role})


def logout_view(request):
    logout(request)
    return redirect('home')