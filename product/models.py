from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=64)
    slug = models.CharField(max_length=128, unique=True)
    brand = models.ForeignKey(
        "brand.Brand", on_delete=models.CASCADE, related_name="brand_products"
    )
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=11, decimal_places=2)
    seller = models.ForeignKey("users.Seller", on_delete=models.CASCADE)
    category = models.ForeignKey(
        to="Category",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="category_products",
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["-created_on"]


class ProductImage(models.Model):
    url = models.URLField(max_length=160)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_images"
    )

    def __str__(self) -> str:
        return self.url


class Category(models.Model):
    name = models.CharField(max_length=12)
    slug = models.CharField(max_length=16)
    image = models.URLField(max_length=160, blank=True, null=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="subcategories",
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "categories"


class ProductSizeQuantity(models.Model):
    product = models.OneToOneField(
        "product.Product", on_delete=models.CASCADE, related_name="size_quantity"
    )
    xs = models.PositiveIntegerField(verbose_name="XS")
    s = models.PositiveIntegerField(verbose_name="S")
    m = models.PositiveIntegerField(verbose_name="M")
    l = models.PositiveIntegerField(verbose_name="L")
    xl = models.PositiveIntegerField(verbose_name="XL")

    def __str__(self) -> str:
        return self.product.name

    class Meta:
        verbose_name_plural = "Product size and quantities"
