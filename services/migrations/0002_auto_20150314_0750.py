# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='cache_duration',
            field=models.IntegerField(default=60, verbose_name=b'Cache expiration'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='service',
            name='check_period',
            field=models.IntegerField(default=60, verbose_name=b'Period of downtime'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='service',
            name='request_timeout',
            field=models.IntegerField(default=30, verbose_name=b'Request timeout'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='service',
            name='store_days',
            field=models.IntegerField(default=7, verbose_name=b'Days to keep data'),
            preserve_default=True,
        ),
    ]
