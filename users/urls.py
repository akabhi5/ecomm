from django.urls import path

from users.views import RegisterUser, customer_login, seller_login

urlpatterns = [
    path("customer/login/", customer_login, name="customer_login"),
    path("seller/login/", seller_login, name="seller_login"),
    path("register/", RegisterUser.as_view(), name="register"),
]
