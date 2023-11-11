from django.contrib import admin

from users.models import Customer, User, Seller


class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "name"]
    list_display_links = ["id", "email", "name"]


class SellerAdmin(admin.ModelAdmin):
    list_display = ["user"]


class CustomerAdmin(admin.ModelAdmin):
    list_display = ["user"]


admin.site.register(User, UserAdmin)
admin.site.register(Seller, SellerAdmin)
admin.site.register(Customer, CustomerAdmin)
