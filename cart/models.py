from django.db import models
from product.models import Product

from users.models import Customer
from django.core.validators import MinValueValidator


class Cart(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)


class CartItemSerializer(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1, message="Quantity cannot be less than 1.")]
    )
