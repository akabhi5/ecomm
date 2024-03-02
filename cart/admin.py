from django.contrib import admin
from cart.models import Cart, CartItem


class CartAdmin(admin.ModelAdmin):
    list_display = ["id", "customer"]


class CartItemAdmin(admin.ModelAdmin):
    list_display = ["id", "cart", "product", "quantity", "size"]


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
