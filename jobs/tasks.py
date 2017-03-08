# -*- coding: utf-8 -*-
# import time
# from celery import Celery
# from celery import shared_task, task
#
#
# @shared_task()
# def add(x, y):
#     print x+y
#     return x+y


# app = Celery('tasks')

# @shared_task
# def add(x, y):
#     return x + y
from __future__ import absolute_import

import os
from celery import shared_task, task
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weitac-gateway.settings')

from django.conf import settings  # noqa

app = Celery('proj')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    # print('Request: {0!r}'.format(self.request))
    print('Request')


# @shared_task
# @app.task(bind=True)
@task
def add(x, y):
    print x, y
    return 'jjjjdjdjdjjd'


if __name__ == '__main__':
    g = add.delay(2, 2)
    print g.id
    print g.result
    print g.status
    # a = debug_task.delay()
    # print a.id
    # print a.result(timeout=10)
