from django.urls import path
from review import views


urlpatterns = [
    path("product/<slug:product_slug>/", views.ReviewAPIView.as_view(), name="review")
]
