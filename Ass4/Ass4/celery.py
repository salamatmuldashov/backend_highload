from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ass4.settings') 

app = Celery('Ass4')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

