from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)

    loyalty_points = models.IntegerField(default=0)
    total_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.name
