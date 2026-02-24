from django.shortcuts import render, redirect
from django.db import transaction
from decimal import Decimal
from .models import Invoice, InvoiceItem
from .forms import InvoiceForm, InvoiceItemForm
from inventory.models import Product
from customers.models import Customer


def invoice_list(req): 
    invoices = Invoice.objects.all() 
    return render(req, 'billing/invoice_list.html', {'invoices': invoices})


def create_invoice(req):

    if req.method == "POST":
        invoice_form = InvoiceForm(req.POST)
        item_form = InvoiceItemForm(req.POST)

        if invoice_form.is_valid() and item_form.is_valid():

            with transaction.atomic():

                invoice_number = invoice_form.cleaned_data['invoice_number']
                discount = invoice_form.cleaned_data.get('discount') or Decimal(0)
                tax = invoice_form.cleaned_data.get('tax') or Decimal(0)

                product = item_form.cleaned_data['product']
                quantity = item_form.cleaned_data['quantity']

                # CREATE OR GET CUSTOMER

                customer = invoice_form.cleaned_data['customer']

                if not customer:
                    name = invoice_form.cleaned_data.get('new_customer_name')
                    # email = invoice_form.cleaned_data.get('new_customer_email')
                    phone = invoice_form.cleaned_data.get('new_customer_phone')


                    if name:
                        customer = Customer.objects.create(
                            name=name,
                            phone=phone,
                        )
                    else:
                        return render(req, 'billing/create_invoice.html', {
                            'invoice_form': invoice_form,
                            'item_form': item_form,
                            'error': "Select existing customer or enter new customer details."
                        })

                # CHECK STOCK

                if product.stock_quantity < quantity:
                    return render(req, 'billing/create_invoice.html', {
                        'invoice_form': invoice_form,
                        'item_form': item_form,
                        'error': "Not enough stock available!"
                    })

                subtotal = product.price * quantity
                total_amount = subtotal
                final_amount = total_amount - discount + tax

                # Get logged-in cashier
                cashier = req.user.staff

                # CREATE INVOICE

                invoice = Invoice.objects.create(
                    invoice_number=invoice_number,
                    customer=customer,
                    cashier=cashier,
                    total_amount=total_amount,
                    discount=discount,
                    tax=tax,
                    final_amount=final_amount
                )

                InvoiceItem.objects.create(
                    invoice=invoice,
                    product=product,
                    quantity=quantity,
                    price=product.price,
                    subtotal=subtotal
                )

                # Deduct stock
                product.stock_quantity -= quantity
                product.save()

                # Update customer stats
                customer.total_spent += final_amount
                customer.loyalty_points += int(final_amount / 100)
                customer.save()

                return redirect('invoice_list')

    else:
        invoice_form = InvoiceForm()
        item_form = InvoiceItemForm()

    return render(req, 'billing/create_invoice.html', {
        'invoice_form': invoice_form,
        'item_form': item_form
    })