from django.db import models
from django.core.validators import MaxValueValidator, MinLengthValidator
from django.utils.translation import gettext_lazy as _

from decimal import Decimal

from shop.models import Product
from coupons.models import Coupon
# Create your models here.


class Order(models.Model):

    coupon = models.ForeignKey(Coupon, 
                               related_name='orders',
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL)
    discount = models.IntegerField(default=0, validators=[MinLengthValidator(0), MaxValueValidator(100)])

    first_name = models.CharField(_("first_name"),max_length=200)
    last_name = models.CharField(_("last_name"),max_length=200)
    transaction_id = models.CharField(max_length=100, null=True, unique=True)
    email = models.EmailField(_("email"),)
    address = models.CharField(_("address"),max_length=400)
    postal_code = models.CharField(_("postal_code"),max_length=20)
    city = models.CharField(_("city"),max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)


    class Meta:
        ordering = ('-created', )
        indexes = [
            models.Index(fields=['-created'])
        ]

    def __str__(self):
        return f"Order {self.id}"

    def get_total_cost(self):
        return self.get_total_cost_before_discount() - self.get_discount()

    def get_total_cost_before_discount(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_discount(self):
        total_cost = self.get_total_cost_before_discount()
        if self.discount:
            return total_cost  * (self.discount / Decimal(100))
        return Decimal(0)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')

    price = models.DecimalField(max_digits=10, decimal_places=2)

    quantity = models.PositiveIntegerField(default=1)


    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.quantity * self.price  
