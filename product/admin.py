from django.contrib import admin
from product.models import Product, ProductImage


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ["id", "name", "slug"]
    list_display_links = ["id", "name"]


class ProductImageAdmin(admin.ModelAdmin):
    model = Product
    list_display = ["id", "url"]
    list_display_links = ["id", "url"]


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
