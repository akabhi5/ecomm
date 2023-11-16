from django.db import IntegrityError
from rest_framework import serializers
from product.models import Product
from review.models import Review
from users.models import Customer
from django.utils.translation import gettext_lazy as _


class ReviewSerializer(serializers.ModelSerializer):
    customer = serializers.CharField(read_only=True)
    product = serializers.CharField(read_only=True)
    customerId = serializers.SerializerMethodField("get_customerId")

    class Meta:
        model = Review
        fields = ["id", "customer", "product", "comment", "customerId"]

    def create(self, validated_data):
        product_slug = self.context["product_slug"]
        product = Product.objects.get(slug=product_slug)
        user = self.context["user"]
        customer = Customer.objects.get(user=user)
        try:
            return Review.objects.create(
                product=product, customer=customer, **validated_data
            )
        except IntegrityError as err:
            raise serializers.ValidationError("You have already reviewed the product")

    def update(self, instance, validated_data):
        comment = validated_data.get("comment")
        user = self.context["user"]
        if user != instance.customer.user:
            raise serializers.ValidationError(
                "You are not authorized to edit this comment"
            )
        instance.comment = comment
        instance.save()
        return instance

    def get_customerId(self, obj):
        return obj.customer.user.id
