from django.contrib import admin

# Register your models here.

from .models import TestCategory

admin.site.register(TestCategory)