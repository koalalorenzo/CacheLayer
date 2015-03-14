from __future__ import absolute_import

import os

from celery import Celery

from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cachelayer.settings.default')

app = Celery('cachelayer')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')

app.conf.update(
    BROKER_URL=settings.CACHES["celery"]["LOCATION"],
    CELERY_RESULT_BACKEND=settings.CACHES["celery"]["LOCATION"],
)

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
