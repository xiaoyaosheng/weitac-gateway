# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_auto_20161222_0544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instance',
            name='instance_id',
            field=models.CharField(max_length=512, null=True),
            preserve_default=True,
        ),
    ]
