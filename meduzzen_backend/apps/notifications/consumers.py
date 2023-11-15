import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from notifications.enums import NotificationStatus
from notifications.models import Notifications


class NotificationsConsumer(WebsocketConsumer):
    def connect(self):
        current_user = self.scope['user']
        # Generate group name for each user
        self.group_name = f'notifications_{current_user.username}_{current_user.id}'
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()

        # Get all notifications of current user
        current_user_notifications_list = Notifications.objects.filter(
            user=current_user
        ).values('id', 'text', 'status')

        for notification in current_user_notifications_list:
            # Add type: 'init_notifications' to keep track of previous notifications
            notification['type'] = 'init_notifications'
            self.send(text_data=json.dumps({'payload': notification}))  

    def receive(self, text_data=None):
        recieved_data_json = json.loads(text_data)
        notification_id = int(recieved_data_json['id'])
        selected_notification = Notifications.objects.get(pk=notification_id)

        if recieved_data_json['type'] == 'mark_read':
            selected_notification.status = NotificationStatus.READ.value
            selected_notification.save()
        else: # If type == 'delete_notification'
            selected_notification.delete()

    def disconnect(self, code):
        self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    def send_notification(self, event):
        data = json.loads(event.get('message'))
        self.send(text_data=json.dumps({'payload': data}))
