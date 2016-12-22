# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0003_instance_host_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='instance',
            old_name='host_id',
            new_name='host',
        ),
        migrations.RenameField(
            model_name='instance',
            old_name='service_id',
            new_name='service',
        ),
    ]
