from django.contrib import admin
from category.models import Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "slug", "parent"]
    list_display_links = ["id", "name", "slug"]


admin.site.register(Category, CategoryAdmin)
