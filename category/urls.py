from django.urls import path

from category.views import CategoryView


urlpatterns = [
    path("products/<slug:category_slug>/", CategoryView.as_view(), name="category")
]
