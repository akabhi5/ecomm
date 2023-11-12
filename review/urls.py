from django.urls import path
from review import views


urlpatterns = [
    path("product/<slug:product_slug>/", views.ReviewView.as_view(), name="reviews")
]
