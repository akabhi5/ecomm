from django.urls import path
from .views import BrandListView, BrandView


urlpatterns = [
    path("<slug:slug>/", BrandView.as_view(), name="brand"),
    path("", BrandListView.as_view(), name="brand-list"),
]
