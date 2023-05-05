from django.contrib import admin
from apps.ProductClass.models import ProductClass

# Register your models here.

admin.site.register(ProductClass,admin.ModelAdmin)