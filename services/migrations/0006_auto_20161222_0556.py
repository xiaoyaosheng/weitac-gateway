# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0005_auto_20161222_0554'),
    ]

    operations = [
        migrations.AddField(
            model_name='instance',
            name='continer_id',
            field=models.CharField(max_length=512, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='instance',
            name='instance_id',
            field=models.CharField(max_length=20, null=True),
            preserve_default=True,
        ),
    ]
