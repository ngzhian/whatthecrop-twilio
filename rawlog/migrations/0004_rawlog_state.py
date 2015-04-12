# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rawlog', '0003_farmdata_raw_log'),
    ]

    operations = [
        migrations.AddField(
            model_name='rawlog',
            name='state',
            field=models.CharField(default='NY', max_length=2),
            preserve_default=False,
        ),
    ]
