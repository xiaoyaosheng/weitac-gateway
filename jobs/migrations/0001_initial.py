# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('service_name', models.CharField(max_length=512)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('info', models.FileField(default={}, upload_to=b'', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
