from django.contrib import admin

# Register your models here.
from sqlviewer.glimpse.models import Model


@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    pass
