from django.contrib import admin

# Register your models here.

from .models import PricingCategory

admin.site.register(PricingCategory)