from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from users.views import RegisterUser

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("register/", RegisterUser.as_view(), name="register"),
    # path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
