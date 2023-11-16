from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import Customer, Seller
from users.serializers import CustomUserSerializer, UserRegisterSerializer

User = get_user_model()


class RegisterUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer


@swagger_auto_schema(method="post", request_body=CustomUserSerializer)
@api_view(["POST"])
def customer_login(request):
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.data.get("email")
        password = serializer.data.get("password")
        user = User.objects.filter(email=email).first()
        if (
            user
            and user.check_password(password)
            and Customer.objects.filter(user=user).exists()
        ):
            refresh = RefreshToken.for_user(user)
            data = {
                "id": user.id,
                "token": str(refresh.access_token),
                "email": user.email,
                "name": user.name,
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(
            {"error": "Invalid username or email"}, status=status.HTTP_401_UNAUTHORIZED
        )
    return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


@swagger_auto_schema(method="post", request_body=CustomUserSerializer)
@api_view(["POST"])
def seller_login(request):
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.data.get("email")
        password = serializer.data.get("password")
        user = User.objects.filter(email=email).first()
        if (
            user
            and user.check_password(password)
            and Seller.objects.filter(user=user).exists()
        ):
            refresh = RefreshToken.for_user(user)
            data = {
                "token": str(refresh.access_token),
                "email": user.email,
                "name": user.name,
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(
            {"error": "Invalid username or email"}, status=status.HTTP_401_UNAUTHORIZED
        )
    return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
