from django.db import models

# Create your models here.
# Abstract model TimeStampedModel
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # abstract = True to enable models inherit from TimeStampedModel
        # https://www.geeksforgeeks.org/how-to-create-abstract-model-class-in-django/
        abstract = True
