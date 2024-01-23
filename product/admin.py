from django.contrib import admin
from product.models import Product, ProductImage, Category, ProductSizeQuantity


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ["id", "name", "slug"]
    list_display_links = ["id", "name"]


class ProductImageAdmin(admin.ModelAdmin):
    model = Product
    list_display = ["id", "url"]
    list_display_links = ["id", "url"]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "slug", "parent"]
    list_display_links = ["id", "name", "slug"]


class ProductSizeQuantityAdmin(admin.ModelAdmin):
    list_display = ["id", "product"]
    list_display_links = ["id", "product"]


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductSizeQuantity, ProductSizeQuantityAdmin)
