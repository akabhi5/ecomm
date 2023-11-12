from django.contrib import admin
from review.models import Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = ["id", "customer", "product"]
    list_display_links = ["id", "customer", "product"]


admin.site.register(Review, ReviewAdmin)
