from django.shortcuts import render, redirect
from django.db import transaction
from decimal import Decimal
from .models import Invoice, InvoiceItem
from .forms import InvoiceForm, InvoiceItemForm
from inventory.models import Product
from customers.models import Customer


def invoice_list(req):
    invoices = Invoice.objects.select_related('customer', 'cashier').prefetch_related(
        'invoiceitem_set__product'
    ).order_by('-created_at')
    return render(req, 'billing/invoice_list.html', {'invoices': invoices})


def create_invoice(req):

    if req.method == "POST":
        invoice_form = InvoiceForm(req.POST)

        # Collect all item rows submitted (product_0, quantity_0, product_1, …)
        items_data = []
        i = 0
        while f'product_{i}' in req.POST:
            form = InvoiceItemForm({
                'product':  req.POST.get(f'product_{i}'),
                'quantity': req.POST.get(f'quantity_{i}'),
            })
            items_data.append(form)
            i += 1

        # Need at least one item row
        if not items_data:
            return render(req, 'billing/create_invoice.html', {
                'invoice_form': invoice_form,
                'error': "Please add at least one product.",
                'products_json': _products_json(),
            })

        forms_valid = invoice_form.is_valid() and all(f.is_valid() for f in items_data)

        if forms_valid:
            with transaction.atomic():
                discount_pct = invoice_form.cleaned_data.get('discount') or Decimal(0)
                tax_pct      = invoice_form.cleaned_data.get('tax')      or Decimal(0)

                # Validate customer
                customer = invoice_form.cleaned_data['customer']
                if not customer:
                    name  = invoice_form.cleaned_data.get('new_customer_name')
                    phone = invoice_form.cleaned_data.get('new_customer_phone')
                    if name:
                        customer = Customer.objects.create(name=name, phone=phone)
                    else:
                        return render(req, 'billing/create_invoice.html', {
                            'invoice_form': invoice_form,
                            'error': "Select an existing customer or enter new customer details.",
                            'products_json': _products_json(),
                        })

                # Validate stock for every item first
                for f in items_data:
                    product  = f.cleaned_data['product']
                    quantity = f.cleaned_data['quantity']
                    if product.stock_quantity < quantity:
                        return render(req, 'billing/create_invoice.html', {
                            'invoice_form': invoice_form,
                            'error': f"Not enough stock for '{product.name}' (available: {product.stock_quantity}).",
                            'products_json': _products_json(),
                        })

                # Calculate totals
                subtotal_total = Decimal(0)
                for f in items_data:
                    product  = f.cleaned_data['product']
                    quantity = f.cleaned_data['quantity']
                    subtotal_total += product.price * quantity

                discount_amt = (subtotal_total * discount_pct / 100).quantize(Decimal('0.01'))
                tax_amt      = (subtotal_total * tax_pct      / 100).quantize(Decimal('0.01'))
                final_amount = subtotal_total - discount_amt + tax_amt

                # Create invoice
                invoice = Invoice.objects.create(
                    invoice_number=invoice_form.cleaned_data['invoice_number'],
                    customer=customer,
                    cashier=req.user.staff,
                    total_amount=subtotal_total,
                    discount=discount_amt,
                    tax=tax_amt,
                    final_amount=final_amount,
                )

                # Create items & deduct stock
                for f in items_data:
                    product  = f.cleaned_data['product']
                    quantity = f.cleaned_data['quantity']
                    subtotal = product.price * quantity
                    InvoiceItem.objects.create(
                        invoice=invoice,
                        product=product,
                        quantity=quantity,
                        price=product.price,
                        subtotal=subtotal,
                    )
                    product.stock_quantity -= quantity
                    product.save()

                # Update customer stats
                customer.total_spent     += final_amount
                customer.loyalty_points  += int(final_amount / 100)
                customer.save()

                return redirect('invoice_list')

        # Re-render with errors
        return render(req, 'billing/create_invoice.html', {
            'invoice_form': invoice_form,
            'items_data': items_data,
            'products_json': _products_json(),
        })

    else:
        invoice_form = InvoiceForm()

    return render(req, 'billing/create_invoice.html', {
        'invoice_form': invoice_form,
        'products_json': _products_json(),
    })


def _products_json():
    """Return product list as JSON string for JS price lookup."""
    import json
    products = Product.objects.values('id', 'name', 'price', 'stock_quantity')
    return json.dumps([
        {'id': p['id'], 'name': p['name'],
         'price': str(p['price']), 'stock': p['stock_quantity']}
        for p in products
    ])