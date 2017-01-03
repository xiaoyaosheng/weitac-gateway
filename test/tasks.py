# tasks.py
import time
from celery import Celery

celery = Celery('tasks', broker='redis://10.6.168.161:6379/0')


@celery.task
def add(x, y):
    return x + y
