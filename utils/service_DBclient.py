import time
from django.utils import timezone


def datetime_to_timestamp(t):
    stamp = int(time.mktime(t.timetuple()))
    return stamp


def save(dic_info):
    print dic_info
    service = dic_info.get('service')
    created_at = datetime_to_timestamp(timezone.now())
    print created_at
    service.created_at = str(created_at)
    service.save()

    instance_list = dic_info.get('instance')
    for instance in instance_list:
        instance.service = service
        instance.save()
