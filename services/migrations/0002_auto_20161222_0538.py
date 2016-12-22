# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('host_name', models.CharField(max_length=20)),
                ('host_ip', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='instance',
            name='host_name',
        ),
        migrations.RemoveField(
            model_name='instance',
            name='service_name',
        ),
        migrations.AddField(
            model_name='instance',
            name='service_id',
            field=models.ForeignKey(to='services.Service', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='instance',
            name='continer_ip',
            field=models.ForeignKey(to='services.IpInfo', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='instance',
            name='instance_id',
            field=models.CharField(max_length=20, null=True),
            preserve_default=True,
        ),
    ]
