from rest_framework import serializers
from review.models import Review
from users.serializers import CustomerSerializer


class ReviewSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()

    class Meta:
        model = Review
        fields = ["id", "customer", "product", "comment"]
