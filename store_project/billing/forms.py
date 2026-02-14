from django import forms
from customers.models import Customer
from .models import InvoiceItem
from inventory.models import Product


class InvoiceItemForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    quantity = forms.IntegerField(min_value=1)

class InvoiceForm(forms.Form):
    invoice_number = forms.CharField(max_length=50)

    # Existing customer
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.all(),
        required=False
    )

    # New customer fields
    new_customer_name = forms.CharField(required=False)
    new_customer_email = forms.EmailField(required=False)
    new_customer_phone = forms.CharField(required=False)

    discount = forms.DecimalField(required=False, initial=0)
    tax = forms.DecimalField(required=False, initial=0)