from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone


def index(req):

    if req.user.is_authenticated:
        return redirect('dashboard')

    if req.method == "POST":
        username = req.POST.get('username')
        password = req.POST.get('password')

        user = authenticate(req, username=username, password=password)

        if user is not None:
            login(req, user)
            return redirect('dashboard')
        else:
            return render(req, 'home/index.html', {
                'error': 'Invalid Username or Password'
            })

    return render(req, 'home/index.html')


@login_required
def dashboard(req):
    role = req.user.staff.role

    from inventory.models import Product
    from customers.models import Customer
    from billing.models import Invoice
    from django.db.models import Sum

    today = timezone.now().date()

    total_products   = Product.objects.count()
    total_customers  = Customer.objects.count()
    total_sales      = Invoice.objects.aggregate(s=Sum('final_amount'))['s'] or 0
    invoices_today   = Invoice.objects.filter(created_at__date=today).count()

    # Low stock products (quantity <= 10)
    low_stock = Product.objects.filter(stock_quantity__lte=10).order_by('stock_quantity')[:5]

    # Recent invoices for activity panel
    recent_invoices = Invoice.objects.select_related('customer', 'cashier').order_by('-created_at')[:5]

    return render(req, 'home/dashboard.html', {
        'role': role,
        'total_products': total_products,
        'total_customers': total_customers,
        'total_sales': total_sales,
        'invoices_today': invoices_today,
        'low_stock': low_stock,
        'recent_invoices': recent_invoices,
    })


def logout_view(req):
    logout(req)
    return redirect('home')