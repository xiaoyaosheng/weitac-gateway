# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_auto_20170207_1038'),
    ]

    operations = [
        migrations.CreateModel(
            name='IpInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(max_length=20)),
                ('is_used', models.BooleanField(default=False)),
                ('gateway_ip', models.CharField(max_length=20)),
                ('subnet_mask', models.CharField(default=24, max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='instance',
            name='continer_ip',
            field=models.ForeignKey(to='services.IpInfo', null=True),
            preserve_default=True,
        ),
    ]
