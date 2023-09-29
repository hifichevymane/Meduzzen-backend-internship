from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

# Create your models here.
# Abstract model TimeStampedModel
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # abstract = True to enable models inherit from TimeStampedModel
        # https://www.geeksforgeeks.org/how-to-create-abstract-model-class-in-django/
        abstract = True

# Custom User model
class User(AbstractUser, TimeStampedModel):
    # Make these fields not to be null
    email = models.EmailField(unique=True, null=False, blank=False)
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)

    # Assing custom model manager
    objects = CustomUserManager()
