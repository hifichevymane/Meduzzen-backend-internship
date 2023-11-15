import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meduzzen_backend.settings')

app = Celery('meduzzen_backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
