from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=12)
    slug = models.CharField(max_length=16)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "categories"
