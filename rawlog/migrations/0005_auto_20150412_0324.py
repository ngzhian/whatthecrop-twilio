# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rawlog', '0004_rawlog_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='farmdata',
            name='media_url',
            field=models.CharField(max_length=500, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='farmdata',
            name='state',
            field=models.CharField(max_length=2, default='NY'),
            preserve_default=False,
        ),
    ]
