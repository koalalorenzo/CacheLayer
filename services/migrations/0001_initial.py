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
                ('name', models.CharField(max_length=50, verbose_name=b'Service Name')),
                ('descrition', models.TextField(null=True, blank=True)),
                ('base_url', models.URLField(null=True, blank=True)),
                ('cache', models.IntegerField(default=60, verbose_name=b'Cache duration (in seconds)')),
                ('check', models.IntegerField(default=60, verbose_name=b'Check period')),
                ('request_timeout', models.IntegerField(default=30, verbose_name=b'HTTP request timeout')),
                ('is_enabled', models.BooleanField(default=False)),
                ('force_down', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('edited', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Service',
                'verbose_name_plural': 'Services',
            },
            bases=(models.Model,),
        ),
    ]
