# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0004_job_describe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='describe',
            field=models.CharField(max_length=512, blank=True),
            preserve_default=True,
        ),
    ]
