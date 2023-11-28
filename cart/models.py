from django.db import models
from product.models import Product

from users.models import Customer
from django.core.validators import MinValueValidator


class Cart(models.Model):
    customer = models.OneToOneField(
        Customer, on_delete=models.CASCADE, related_name="customer_cart"
    )

    def __str__(self):
        return f"{self.customer.user.name} - cart"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1, message="Quantity cannot be less than 1.")]
    )

    def __str__(self):
        return str(self.id)

    class Meta:
        unique_together = (
            "cart",
            "product",
        )
