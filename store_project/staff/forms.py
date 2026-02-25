from django import forms
from django.contrib.auth.models import User
from .models import Staff


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['role', 'salary', 'phone']

class UpdateStaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['role', 'salary', 'phone']

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
