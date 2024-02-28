from django.contrib import admin
from wishlist.models import Wishlist, WishlistItem


class WishlistAdmin(admin.ModelAdmin):
    list_display = ["id", "customer"]


class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ["id", "wishlist", "product"]


admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(WishlistItem, WishlistItemAdmin)
