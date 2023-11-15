from django.urls import path
from product import views


urlpatterns = [
    path("category/", views.CategoryView.as_view(), name="categories"),
    path(
        "category/<slug:category_slug>/",
        views.CategoryProductView.as_view(),
        name="category_product",
    ),
    path("<slug:slug>/", views.ProductDetail.as_view(), name="product-detail"),
    path("", views.ProductList.as_view(), name="products"),
]
