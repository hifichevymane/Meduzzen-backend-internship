from api.models import TimeStampedModel
from django.contrib.auth import get_user_model
from django.db import models

# User model
User = get_user_model()

# Create your models here.
class Company(TimeStampedModel):
    VISIBILITY_CHOICES = (
        ('hidden', 'Hidden'),
        ('visible', 'Visible for all'),
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=False, null=False, unique=True)
    description = models.TextField(blank=False, null=False)
    visibility = models.CharField(max_length=15, 
                                  choices=VISIBILITY_CHOICES, 
                                  default='visible')

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = 'Companies' # Plural naming

    def __str__(self):
        return self.name    
