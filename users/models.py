from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from cart.models import Cart

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        CUSTOMER = "CU", _("Customer")
        SELLER = "SE", _("Seller")

    name = models.CharField(max_length=16)
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=2, choices=Role.choices, default=Role.CUSTOMER)
    address = models.CharField(max_length=160)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    pickup_address = models.CharField(max_length=160)

    def __str__(self) -> str:
        return self.user.name


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self) -> str:
        return self.user.name


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == User.Role.CUSTOMER:
            customer = Customer.objects.create(user=instance)
            Cart.objects.create(customer=customer)
        elif instance.role == User.Role.SELLER:
            Seller.objects.create(user=instance)
