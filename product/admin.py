from django.contrib import admin
from product.models import Product


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ["id", "name", "slug"]
    list_display_links = ["id", "name"]


admin.site.register(Product, ProductAdmin)
