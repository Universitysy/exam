from django.contrib import admin
from .models import *

class CustomUserAdmin(admin.ModelAdmin):
    class Meta:
        model = CustomUser
        list_display = ['get_full_name']




admin.site.register(CustomUser, CustomUserAdmin)

