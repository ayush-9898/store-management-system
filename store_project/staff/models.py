from django.db import models
from django.contrib.auth.models import User


class Staff(models.Model):

    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Manager', 'Manager'),
        ('Cashier', 'Cashier'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    phone = models.CharField(max_length=10)
    joining_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
