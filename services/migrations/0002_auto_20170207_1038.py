# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='instance',
            name='command',
            field=models.CharField(max_length=512, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='instance',
            name='environment',
            field=models.CharField(max_length=512, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='instance',
            name='hostname',
            field=models.CharField(max_length=512, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='instance',
            name='volumes',
            field=models.CharField(max_length=512, null=True),
            preserve_default=True,
        ),
    ]
