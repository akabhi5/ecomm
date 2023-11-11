from django.contrib.auth import get_user_model
from rest_framework import generics

from users.serializers import UserRegisterSerializer

User = get_user_model()


class RegisterUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
