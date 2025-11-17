from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'awd_main.settings')
#Sets up the new celery application for our django project 'awd_main' 
app = Celery('awd_main')
#namespace='celery' means all celery-related configuration keys 
app.config_from_object('django.conf:settings', namespace='CELERY')
#load task module from all registered django apps
app.autodiscover_tasks()

@app.task(bind=True,ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')