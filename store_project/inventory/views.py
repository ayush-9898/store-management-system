from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Supplier
from .forms import ProductForm,updateForm,supplierForm


def product_list(req):
    products = Product.objects.all()
    return render(req, 'inventory/product_list.html', {'products': products})


def add_product(req):
    if req.method == "POST":
        form = ProductForm(req.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()

    return render(req, 'inventory/add_product.html', {'form': form})


def update_product(req,id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return HttpResponse("Product not found")
    if req.method=="POST":
        form=updateForm(req.POST,instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form=updateForm(instance=product)
    return render(req,'inventory/update_product.html',{'form':form})


def delete_product(req, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return HttpResponse("Product not found")
    if req.method == "POST":
        product.delete()
        return redirect('product_list')
    return render(req, 'inventory/delete_product.html', {'product': product})


# ── Supplier Views ─────────────────────────────────────────

def supplier_list(req):
    suppliers = Supplier.objects.all()
    return render(req, 'inventory/supplier_list.html', {'suppliers': suppliers})


def add_supplier(req):
    if req.method == "POST":
        form = supplierForm(req.POST)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = supplierForm()
    return render(req, 'inventory/add_supplier.html', {'form': form})


def update_supplier(req, id):
    try:
        supplier= Supplier.objects.get(id=id)
    except Supplier.DoesNotExist:
        return HttpResponse("supplier not found")
    if req.method == "POST":
        form = supplierForm(req.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = supplierForm(instance=supplier)
    return render(req, 'inventory/update_supplier.html', {'form': form, 'supplier': supplier})


def delete_supplier(req, id):
    try:
        supplier= Supplier.objects.get(id=id)
    except Supplier.DoesNotExist:
        return HttpResponse("Supplier not found")
    if req.method == "POST":
        supplier.delete()
        return redirect('supplier_list')
    return render(req, 'inventory/delete_supplier.html', {'supplier': supplier})


# ── Low Stock Alert ────────────────────────────────────────

def send_low_stock_alert(req):
    """Manual trigger: Admin clicks 'Send Alert' button on product list page."""

    low_stock = Product.objects.filter(
        stock_quantity__lte=F('reorder_level')
    ).select_related('supplier')

    if not low_stock.exists():
        messages.success(req, 'All products are well stocked. No alert sent.')
        return redirect('product_list')

    # # Build email body
    # lines = []
    # lines.append('The following products are at or below their reorder level:\n')
    # lines.append(f'{"Product":<30} {"SKU":<15} {"Stock":>7} {"Reorder":>8} {"Supplier":<20} Status')
    # lines.append('-' * 95)

    # for p in low_stock:
    #     supplier_name = p.supplier.name if p.supplier else 'N/A'
    #     status = 'OUT OF STOCK' if p.stock_quantity == 0 else 'LOW STOCK'
    #     lines.append(
    #         f'{p.name:<30} {p.SKU:<15} {p.stock_quantity:>7} {p.reorder_level:>8} '
    #         f'{supplier_name:<20} [{status}]'
    #     )

    # lines.append(f'\nTotal products needing attention: {low_stock.count()}')
    # lines.append('\nThis is an alert from PEP Store Management System.')

    # body = '\n'.join(lines)
    # subject = f'[PEP Store] ⚠ Low Stock Alert — {low_stock.count()} product(s) need restocking'

    # recipients = getattr(settings, 'LOW_STOCK_ALERT_RECIPIENTS', [])
    # if not recipients:
    #     messages.error(req, 'LOW_STOCK_ALERT_RECIPIENTS is not set in settings.py.')
    #     return redirect('product_list')

    # try:
    #     send_mail(
    #         subject=subject,
    #         message=body,
    #         from_email=settings.DEFAULT_FROM_EMAIL,
    #         recipient_list=recipients,
    #         fail_silently=False,
    #     )
    #     messages.success(
    #         req,
    #         f'Low stock alert sent to {", ".join(recipients)} — {low_stock.count()} product(s) reported.'
    #     )
    # except Exception as e:
    #     messages.error(req, f'Failed to send email: {e}')

    # return redirect('product_list')