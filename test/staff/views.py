from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import Staff
from .forms import UserForm, StaffForm
from .decorators import role_required


def staff_list(request):
    staff_members = Staff.objects.all()
    return render(request, 'staff/list_staff.html', {'staff_members': staff_members})


@role_required(allowed_roles=['Admin'])
def add_staff(request):

    if request.method == "POST":
        user_form = UserForm(request.POST)
        staff_form = StaffForm(request.POST)

        if user_form.is_valid() and staff_form.is_valid():

            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()

            staff = staff_form.save(commit=False)
            staff.user = user
            staff.save()

            return redirect('staff_list')

    else:
        user_form = UserForm()
        staff_form = StaffForm()

    return render(request, 'staff/add_staff.html', {
        'user_form': user_form,
        'staff_form': staff_form
    })
