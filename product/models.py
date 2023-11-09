from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=64)
    slug = models.CharField(max_length=128)
    image_url = models.CharField(max_length=160)
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["-created_on"]
