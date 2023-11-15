
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Notifications
from .schemas.notifications import NotificationMessageBodySchema, SendWebsocketNotificationBodySchema


@receiver(post_save, sender=Notifications)
def send_websocket_notification(sender, instance: Notifications, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        group_name = f'notifications_{instance.user.username}_{instance.user.id}'
        
        group_message = SendWebsocketNotificationBodySchema(
            type='send_notification',
            message=NotificationMessageBodySchema(
                id=instance.id,
                status=instance.status,
                text=instance.text
            ).model_dump_json()
        )
        
        async_to_sync(channel_layer.group_send)(group_name, group_message.model_dump())
