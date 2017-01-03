from django.db import models

# Create your models here.
import django.utils

class Job(models.Model):
    service_name = models.CharField(max_length=512)

    updated_at = models.DateTimeField(auto_now=True)

    info = models.FileField(default={}, blank=True)