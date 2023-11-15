from api.models import TimeStampedModel
from django.contrib.auth import get_user_model
from django.db import models

from notifications.enums import NotificationStatus

User = get_user_model()

# Create your models here.
class Notifications(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(null=False, blank=False)
    status = models.CharField(
        choices=NotificationStatus.choices(), 
        default=NotificationStatus.UNREAD.value
    )

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
    
    def __str__(self) -> str:
        return f'{self.text} - {self.status}'
