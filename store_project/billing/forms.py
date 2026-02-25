from django import forms
from customers.models import Customer
from inventory.models import Product


class InvoiceForm(forms.Form):
    invoice_number = forms.CharField(max_length=50)

    customer = forms.ModelChoiceField(
        queryset=Customer.objects.all(),
        required=False
    )
    new_customer_name  = forms.CharField(required=False)
    new_customer_phone = forms.CharField(required=False)

    # Now percentage (0–100)
    discount = forms.DecimalField(
        required=False, initial=0,
        min_value=0, max_value=100,
        decimal_places=2
    )
    tax = forms.DecimalField(
        required=False, initial=0,
        min_value=0, max_value=100,
        decimal_places=2
    )


class InvoiceItemForm(forms.Form):
    product  = forms.ModelChoiceField(queryset=Product.objects.all())
    quantity = forms.IntegerField(min_value=1)