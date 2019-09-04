from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from devices.tasks import add
from celery.schedules import crontab
from datetime import timedelta

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'easy_cmdb.settings')

app = Celery('easy_cmdb')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
app.conf.update(
    CELERYBATE_SCHEDULE={
        'sum-task': 'add',
        'schedule': timedelta(seconds=20),
        'args': (5, 6)
    }
)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
