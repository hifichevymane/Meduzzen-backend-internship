import logging
from django.db import models

# Logging all models actions
logger = logging.getLogger('main')


# Create your models here.
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Adding a record
    def save(self, *args, **kwargs):
        logger.info('The record has been added')
        super(TimeStampedModel, self).save(*args, **kwargs)
