from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=32)
    image = models.URLField()
    description = models.TextField()
    slug = models.SlugField(max_length=48, unique=True)
    seller = models.ForeignKey("users.Seller", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name
