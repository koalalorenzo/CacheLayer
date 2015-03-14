# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name=b'Name')),
                ('domain', models.CharField(max_length=60, null=True, verbose_name=b'Domain', blank=True)),
                ('descrition', models.TextField(null=True, blank=True)),
                ('store_days', models.IntegerField(default=7, verbose_name=b'Days to keep data')),
                ('check_period', models.IntegerField(default=60, verbose_name=b'Period of downtime')),
                ('request_timeout', models.IntegerField(default=30, verbose_name=b'Request timeout')),
                ('cache_duration', models.IntegerField(default=60, verbose_name=b'Cache expiration')),
                ('is_enabled', models.BooleanField(default=False)),
                ('force_down', models.BooleanField(default=False)),
                ('is_crawler_enabled', models.BooleanField(default=False)),
                ('crawled_at', models.DateTimeField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('edited_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Service',
                'verbose_name_plural': 'Services',
            },
            bases=(models.Model,),
        ),
    ]
