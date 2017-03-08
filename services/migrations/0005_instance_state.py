# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='instance',
            name='state',
            field=models.CharField(max_length=20, null=True),
            preserve_default=True,
        ),
    ]
