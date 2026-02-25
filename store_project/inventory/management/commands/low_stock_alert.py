from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.db.models import F
from django.conf import settings
from inventory.models import Product


class Command(BaseCommand):
    help = 'Send a low stock alert email for products at or below reorder level'

    def handle(self, *args, **kwargs):

        low_stock = Product.objects.filter(
            stock_quantity__lte=F('reorder_level')
        ).select_related('category', 'supplier')

        if not low_stock.exists():
            self.stdout.write(self.style.SUCCESS('All products are well stocked. No alert sent.'))
            return

        # ── Build plain-text email body ───────────────────
        lines = []
        lines.append('The following products are at or below their reorder level:\n')
        lines.append(f'{"Product":<30} {"SKU":<15} {"Stock":>7} {"Reorder":>8} {"Supplier":<20} Status')
        lines.append('-' * 95)

        for p in low_stock:
            supplier_name = p.supplier.name if p.supplier else 'N/A'
            status = 'OUT OF STOCK' if p.stock_quantity == 0 else 'LOW STOCK'
            lines.append(
                f'{p.name:<30} {p.SKU:<15} {p.stock_quantity:>7} {p.reorder_level:>8} '
                f'{supplier_name:<20} [{status}]'
            )

        lines.append('\n' + '-' * 95)
        lines.append(f'Total products needing attention: {low_stock.count()}')
        lines.append('\nThis is an automated alert from PEP Store Management System.')
        lines.append('Please restock the above items as soon as possible.')

        body = '\n'.join(lines)
        subject = f'[PEP Store] ⚠ Low Stock Alert — {low_stock.count()} product(s) need restocking'

        recipients = getattr(settings, 'LOW_STOCK_ALERT_RECIPIENTS', [])
        if not recipients:
            self.stderr.write(
                self.style.ERROR('LOW_STOCK_ALERT_RECIPIENTS is not set in settings.py')
            )
            return

        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipients,
            fail_silently=False,
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'✓ Alert sent to {recipients} — {low_stock.count()} low-stock product(s) reported.'
            )
        )