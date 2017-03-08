import time
from django.utils import timezone
from services.models import Instance
from services.models import IpInfo, Agent
import datetime


def update_instance(instance_name, status):
    instance = Instance.objects.get(name=instance_name)
    instance.state = status
    instance.save()
