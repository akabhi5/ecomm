from django.urls import path

from cart import views


urlpatterns = [
    path("<slug:product>/", views.CartDetailView.as_view(), name="cart-detail"),
    path("", views.CartView.as_view(), name="cart"),
]
