from django.http import Http404
from review.serializers import ReviewSerializer
from review.models import Review
from users.models import Customer
from users.permissions import IsCustomer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import permissions


class ReviewAPIView(APIView):
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_object(self, product_slug):
        try:
            return Review.objects.get(product__slug=product_slug)
        except Review.DoesNotExist:
            raise Http404

    def get(self, request, product_slug, format=None):
        reviews = Review.objects.filter(product__slug=product_slug)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "comment": openapi.Schema(
                    type=openapi.TYPE_STRING, description="string"
                ),
            },
        ),
    )
    def post(self, request, product_slug, format=None):
        serializer = ReviewSerializer(
            data=request.data,
            context={"user": request.user, "product_slug": product_slug},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "comment": openapi.Schema(
                    type=openapi.TYPE_STRING, description="string"
                ),
            },
        ),
    )
    def put(self, request, product_slug, format=None):
        customer = Customer.objects.get(user=self.request.user)
        review = Review.objects.get(product__slug=product_slug, customer=customer)
        serializer = ReviewSerializer(
            review,
            data=request.data,
            context={"user": request.user},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_slug, format=None):
        customer = Customer.objects.get(user=self.request.user)
        review = Review.objects.get(product__slug=product_slug, customer=customer)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
