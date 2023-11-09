from django.urls import path
from product import views


urlpatterns = [
    path("", views.ProductList.as_view(), name="products")
]