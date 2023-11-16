import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meduzzen_backend.settings')

app = Celery('meduzzen_backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_quiz_reminder_notification_every_24_hours': {
        'task': 'quizzes.tasks.send_beat_reminder_quiz_notification',
        'schedule': crontab(minute=0, hour=0) # Execute task every 24 hour at midnight
    }
}
