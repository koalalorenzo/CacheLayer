# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('domain', models.CharField(max_length=60, verbose_name='Domain')),
                ('descrition', models.TextField(null=True, blank=True)),
                ('store_days', models.IntegerField(verbose_name='Days to keep data', default=7)),
                ('check_period', models.IntegerField(verbose_name='Period of downtime', default=60)),
                ('request_timeout', models.IntegerField(verbose_name='Request timeout', default=30)),
                ('cache_duration', models.IntegerField(verbose_name='Cache expiration', default=60)),
                ('is_enabled', models.BooleanField(default=False)),
                ('force_down', models.BooleanField(default=False)),
                ('is_crawler_enabled', models.BooleanField(default=False)),
                ('crawled_at', models.DateTimeField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('edited_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Service',
                'verbose_name_plural': 'Services',
            },
            bases=(models.Model,),
        ),
    ]
