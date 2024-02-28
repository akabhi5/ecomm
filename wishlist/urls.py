from django.urls import path

from wishlist import views


urlpatterns = [
    path(
        "wishlist-items/<slug:product_slug>/",
        views.WishlistItemsUpdateView.as_view(),
        name="wishlist-item-detail",
    ),
    path("wishlist-items/", views.WishlistItemsView.as_view(), name="wishlist-items"),
]
