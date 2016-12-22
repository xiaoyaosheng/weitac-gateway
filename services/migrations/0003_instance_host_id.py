# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_auto_20161222_0538'),
    ]

    operations = [
        migrations.AddField(
            model_name='instance',
            name='host_id',
            field=models.ForeignKey(to='services.Agent', null=True),
            preserve_default=True,
        ),
    ]
