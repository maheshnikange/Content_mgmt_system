from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Permission

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=10)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    pincode = models.CharField(max_length=6)

class ContentItem(models.Model):
    title = models.CharField(max_length=30)
    body = models.CharField(max_length=300)
    summary = models.CharField(max_length=60)
    document = models.FileField(upload_to='documents/')
    # categories = models.ManyToManyField('Category')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # class Meta:
    #         permissions = [
    #             ("can_create_content", "Can create content"),
    #             # ... other permissions ...
    #         ]
