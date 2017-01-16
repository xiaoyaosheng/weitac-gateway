# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_auto_20170103_1537'),
    ]

    operations = [
        migrations.RenameField(
            model_name='job',
            old_name='service_name',
            new_name='job_name',
        ),
    ]
