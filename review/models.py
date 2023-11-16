from django.db import models
from users.models import Customer
from product.models import Product


class Review(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.TextField()

    class Meta:
        unique_together = (
            "customer",
            "product",
        )

    def __str__(self) -> str:
        return f"{self.customer} - {self.product}"
