import logging

from django.contrib.auth import get_user_model
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

# Get User model
User = get_user_model()

# Get 'signals' logger
logger = logging.getLogger('models')

# Log adding User model instance
@receiver(post_save, sender=User)
def log_user_creation(sender, instance, **kwargs):
    logger.info('The User instance has been added/updated successfully!')

# Log deleting User model instance
@receiver(post_delete, sender=User)
def log_user_deletion(sender, instance, **kwargs):
    logger.info('The User instance has been deleted successfully!')
