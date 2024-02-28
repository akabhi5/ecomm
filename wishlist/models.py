from django.db import models


class Wishlist(models.Model):
    customer = models.OneToOneField(
        "users.Customer", on_delete=models.CASCADE, related_name="customer_wishlist"
    )

    def __str__(self):
        return f"{self.customer.user.name} - wishlist"


class WishlistItem(models.Model):
    wishlist = models.ForeignKey(
        Wishlist, on_delete=models.CASCADE, related_name="wishlist_items"
    )
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    class Meta:
        unique_together = (
            "wishlist",
            "product",
        )
