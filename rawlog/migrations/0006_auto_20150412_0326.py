# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rawlog', '0005_auto_20150412_0324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmdata',
            name='media_url',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
