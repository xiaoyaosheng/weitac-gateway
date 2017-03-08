from __future__ import unicode_literals
from django.db import models
# from redisco import models
from json_field.fields import JSONField
from django.utils import timezone


# Create your models here.
class IpInfo(models.Model):
    address = models.CharField(max_length=20)
    is_used = models.BooleanField(default=False)
    gateway_ip = models.CharField(max_length=20)
    subnet_mask = models.CharField(max_length=20,default=24)


class Agent(models.Model):
    host_name = models.CharField(max_length=20)
    host_ip = models.CharField(max_length=20)


class Service(models.Model):
    service_name = models.CharField(max_length=512)
    instance_amount = models.IntegerField()
    image_name = models.CharField(max_length=512)
    created_at = models.CharField(max_length=512, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    details = JSONField(default={}, blank=True)
    finished_at = models.IntegerField(default=0)


class Instance(models.Model):
    name = models.CharField(max_length=512)
    service = models.ForeignKey(Service, null=True)
    instance_id = models.CharField(max_length=20, null=True)
    continer_id = models.CharField(max_length=512, null=True)
    continer_ip = models.ForeignKey(IpInfo, null=True)
    # image_name = models.CharField(max_length=512)
    created_at = models.CharField(max_length=512, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    host = models.ForeignKey(Agent, null=True)
    details = JSONField(default={}, blank=True)
    command = models.CharField(max_length=512, null=True)
    hostname = models.CharField(max_length=512, null=True)
    volumes = models.CharField(max_length=512, null=True)
    environment = models.CharField(max_length=512, null=True)
    state = models.CharField(max_length=20,null=True)

# app_id = models.CharField(db_index=True, max_length=512)
#     finished_at = models.IntegerField(default=0)
#     survived_day = models.DateField(default=datetime.date.today)
#     size = models.CharField(max_length=256, default='None')
#     app_info = models.ForeignKey(AppSizeInfo, null=True)
#     category = models.CharField(default='service', max_length=7)
# #     details = models.CharField(max_length=512, null=True)

# def is_finished(self):
#     return self.finished_at != 0
#
# class Meta:
#     unique_together = ('instance_id', 'survived_day')


class Image(models.Model):
    name = models.CharField(max_length=512)
    project = models.CharField(max_length=512)
    repository = models.CharField(max_length=512)
    tag = models.CharField(max_length=512)
    registry = models.CharField(max_length=512, default='docker.weitac.com')

