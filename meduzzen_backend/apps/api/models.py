from django.contrib.auth.models import AbstractUser
from django.db import models

from api.managers import CustomUserManager


# Create your models here.
# Abstract model TimeStampedModel
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # abstract = True to enable models inherit from TimeStampedModel
        abstract = True

# Custom User model
class User(AbstractUser, TimeStampedModel):
    # Make these fields not to be null
    email = models.EmailField(unique=True, null=False, blank=False)
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    image_path = models.ImageField(upload_to='img', default='profile-pic.webp')

    # Assing base user manager for admin panel
    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
