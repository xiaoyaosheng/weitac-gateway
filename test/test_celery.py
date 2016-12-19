from celery import Celery

app = Celery('tasks', broker='redis://10.6.168.161')
# BROKER_URL = 'redis://:password@hostname:port/db_number'
# BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}  # 1 hour.

@app.task
def set_email(x, y):
    print('sending mail to %s...')
    return x + y
