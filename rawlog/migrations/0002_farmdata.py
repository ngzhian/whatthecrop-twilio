# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rawlog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FarmData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crop', models.CharField(max_length=200)),
                ('pest', models.CharField(max_length=200)),
                ('harvest', models.CharField(max_length=200)),
            ],
        ),
    ]
