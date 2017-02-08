import time
from django.utils import timezone
from services.models import Instance
from services.models import IpInfo
import datetime


def datetime_to_timestamp(t):
    stamp = int(time.mktime(t.timetuple()))
    return stamp


def save(dic_info):
    print dic_info
    service = dic_info.get('service')
    # created_at = datetime_to_timestamp(timezone.now())
    # created_at = timezone.now()
    created_at = datetime.datetime.now()
    print created_at
    service.created_at = created_at
    service.save()

    instance_list = dic_info.get('instance')
    for instance in instance_list:
        instance.service = service
        instance.save()


def change_db_ip(instance_name, ip, subnet_mask, gateway_ip):
    # print (instance_name, ip, subnet_mask, gateway_ip)
    instance = Instance.objects.get(name=instance_name)
    ipinfo = IpInfo.objects.get_or_create(address=ip,subnet_mask=subnet_mask,gateway_ip=gateway_ip)
    print ipinfo
    print instance
    instance.continer_ip = ipinfo[0]
    instance.save()
