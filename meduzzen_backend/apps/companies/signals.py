import logging

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Company

# Get 'signals' logger
logger = logging.getLogger('models')

# Log adding/updating Company model instance
@receiver(post_save, sender=Company)
def log_company_creation(sender, instance, **kwargs):
    logger.info('The Company instance has been added/updated successfully!')

# Log deleting Company model instance
@receiver(post_delete, sender=Company)
def log_company_deletion(sender, instance, **kwargs):
    logger.info('The Company instance has been deleted successfully!')
