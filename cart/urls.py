from django.urls import path

from cart import views


urlpatterns = [
    # path("<slug:product>/", views.CartDetailView.as_view(), name="cart-detail"),
    # path("", views.CartView.as_view(), name="cart"),
    path(
        "cart-items/<slug:product_slug>/<str:size>/",
        views.CartItemsUpdateView.as_view(),
        name="cart-items-detail",
    ),
    path("cart-items/", views.CartItemsView.as_view(), name="cart-items"),
    path("cart-total/", views.CartTotalAmount.as_view(), name="cart-total"),
]
