from django.contrib import admin
from .models import CustomUser,ContentItem

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(ContentItem)