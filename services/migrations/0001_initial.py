# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import json_field.fields


class Migration(migrations.Migration):

    dependencies = [
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
        migrations.CreateModel(
            name='Instance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=512)),
                ('instance_id', models.CharField(max_length=20, null=True)),
                ('continer_id', models.CharField(max_length=512, null=True)),
                ('continer_ip', models.CharField(max_length=512, null=True)),
                ('created_at', models.CharField(max_length=512, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('details', json_field.fields.JSONField(default={}, help_text='Enter a valid JSON object', blank=True)),
                ('host', models.ForeignKey(to='services.Agent', null=True)),
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
                ('created_at', models.CharField(max_length=512, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('details', json_field.fields.JSONField(default={}, help_text='Enter a valid JSON object', blank=True)),
                ('finished_at', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='instance',
            name='service',
            field=models.ForeignKey(to='services.Service', null=True),
            preserve_default=True,
        ),
    ]
