# -*- coding: utf-8 -*-
import time
from celery import Celery
from celery import shared_task,task


@task()
def add(x, y):
    return x + y


# app = Celery('tasks')

# @shared_task
# def add(x, y):
#     return x + y