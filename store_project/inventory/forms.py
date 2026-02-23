from django import forms
from .models import Product,Supplier

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class updateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','price','supplier','stock_quantity']


class supplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'