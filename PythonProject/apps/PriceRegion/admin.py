from django.contrib import admin
from apps.PriceRegion.models import PriceRegion

# Register your models here.

admin.site.register(PriceRegion,admin.ModelAdmin)