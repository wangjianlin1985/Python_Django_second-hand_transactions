from django.contrib import admin
from apps.OldLevel.models import OldLevel

# Register your models here.

admin.site.register(OldLevel,admin.ModelAdmin)