from django.shortcuts import render, redirect
from .models import Customer
# from .forms import CustomerForm


def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customers/customer_list.html', {'customers': customers})


