from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Staff
from .forms import UserForm, StaffForm, UpdateUserForm, UpdateStaffForm
from .decorators import role_required


def staff_list(req):
    staff_members = Staff.objects.all()
    return render(req, 'staff/list_staff.html', {'staff_members': staff_members})


@role_required(allowed_roles=['Admin'])
def add_staff(req):

    if req.method == "POST":
        user_form = UserForm(req.POST)
        staff_form = StaffForm(req.POST)

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

    return render(req, 'staff/add_staff.html', {
        'user_form': user_form,
        'staff_form': staff_form
    })


@role_required(allowed_roles=['Admin'])
def update_staff(req,id):
    try:
        staff= Staff.objects.get(id=id)
    except Staff.DoesNotExist:
        return HttpResponse("staff not found")

    if req.method == "POST":
        user_form = UpdateUserForm(req.POST, instance=staff.user)
        staff_form = UpdateStaffForm(req.POST, instance=staff)

        if user_form.is_valid() and staff_form.is_valid():
            user_form.save()
            staff_form.save()
            return redirect('staff_list')
    else:
        user_form = UpdateUserForm(instance=staff.user)
        staff_form = UpdateStaffForm(instance=staff)

    return render(req, 'staff/update_staff.html', {
        'user_form': user_form,
        'staff_form': staff_form,
        'staff': staff,
    })


@role_required(allowed_roles=['Admin'])
def delete_staff(req,id):
    try:
        staff= Staff.objects.get(id=id)
    except Staff.DoesNotExist:
        return HttpResponse("staff not found")

    # Prevent admin from deleting themselves
    if staff.user == req.user:
        return redirect('staff_list')

    if req.method == "POST":
        user = staff.user
        staff.delete()
        user.delete()
        return redirect('staff_list')

    return render(req, 'staff/delete_staff.html', {'staff': staff})
