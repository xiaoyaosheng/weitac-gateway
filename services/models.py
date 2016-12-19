from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Service(models.Model):
    name =
    service_name =
    instance_id = models.CharField(max_length=512)
    image_name =
    created_at = models.IntegerField(default=0)
    updated_at = models.IntegerField(default=0)
    host_name =
    continer_ip =

    app_id = models.CharField(db_index=True, max_length=512)
    finished_at = models.IntegerField(default=0)
    survived_day = models.DateField(default=datetime.date.today)
    size = models.CharField(max_length=256, default='None')
    app_info = models.ForeignKey(AppSizeInfo, null=True)
    category = models.CharField(default='service', max_length=7)
#     details = models.CharField(max_length=512, null=True)

    def is_finished(self):
        return self.finished_at != 0

    class Meta:
        unique_together = ('instance_id', 'survived_day')