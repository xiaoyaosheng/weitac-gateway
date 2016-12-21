# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import json_field.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Instance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=512)),
                ('service_name', models.CharField(max_length=512)),
                ('continer_ip', models.CharField(max_length=20, null=True)),
                ('instance_id', models.IntegerField()),
                ('image_name', models.CharField(max_length=512)),
                ('created_at', models.IntegerField(default=0)),
                ('updated_at', models.IntegerField(default=0)),
                ('host_name', models.CharField(max_length=512)),
                ('details', json_field.fields.JSONField(default={}, help_text='Enter a valid JSON object', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IpInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('is_used', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('service_name', models.CharField(max_length=512)),
                ('instance_amount', models.IntegerField()),
                ('image_name', models.CharField(max_length=512)),
                ('created_at', models.IntegerField(default=0)),
                ('updated_at', models.IntegerField(default=0)),
                ('details', json_field.fields.JSONField(default={}, help_text='Enter a valid JSON object', blank=True)),
                ('finished_at', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
