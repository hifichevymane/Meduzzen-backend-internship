from notifications.enums import NotificationStatus
from pydantic import BaseModel


class NotificationMessageBodySchema(BaseModel):
    id: int # Notification id
    status: NotificationStatus
    text: str


class SendWebsocketNotificationBodySchema(BaseModel):
    type: str
    message: str # We will pass NotificationMessageBodySchema and call model_dump_json()
