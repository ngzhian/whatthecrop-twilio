# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rawlog', '0002_farmdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='farmdata',
            name='raw_log',
            field=models.OneToOneField(default=1, to='rawlog.RawLog'),
            preserve_default=False,
        ),
    ]
