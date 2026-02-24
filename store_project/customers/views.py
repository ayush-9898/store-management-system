from django.shortcuts import render, redirect
from .models import Customer
# from .forms import CustomerForm


def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customers/customer_list.html', {'customers': customers})


# def add_customer(request):

#     if request.method == "POST":
#         form = CustomerForm(request.POST)

#         if form.is_valid():
#             form.save()
#             return redirect('customer_list')

#     else:
#         form = CustomerForm()

#     return render(request, 'customers/add_customer.html', {'form': form})
