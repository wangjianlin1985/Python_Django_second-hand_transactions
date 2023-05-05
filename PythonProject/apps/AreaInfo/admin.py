from django.contrib import admin
from apps.AreaInfo.models import AreaInfo

# Register your models here.

admin.site.register(AreaInfo,admin.ModelAdmin)