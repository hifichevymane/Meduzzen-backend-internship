import logging
from django.db.models.signals import post_save, post_delete, pre_delete, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

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
def log_user_creation(sender, instance, **kwargs):
    logger.info('The User instance has been deleted successfully!')
