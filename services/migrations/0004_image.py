# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0003_auto_20170208_1503'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=512)),
                ('project', models.CharField(max_length=512)),
                ('repository', models.CharField(max_length=512)),
                ('tag', models.CharField(max_length=512)),
                ('registry', models.CharField(default='docker.weitac.com', max_length=512)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
