from django.db import models

# Create your models here.
class Configuration(models.Model):
    configuration_name = models.CharField(max_length=512)

    updated_at = models.DateTimeField(auto_now=True)

    info = models.BinaryField(default={}, blank=True)
    # info = models.CharField(max_length=512)
    describe=models.CharField(max_length=512,blank=True)