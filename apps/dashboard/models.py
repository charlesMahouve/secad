from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class PricingCategory(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)

    made_by = models.ForeignKey(User, related_name='PricingCategories', on_delete=models.CASCADE)
    made_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'PricingCategories'

    def __str__(self):
        return self.title
