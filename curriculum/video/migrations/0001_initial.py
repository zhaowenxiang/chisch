# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('chapter', models.SmallIntegerField()),
                ('hour', models.SmallIntegerField()),
                ('title', models.CharField(max_length=100)),
                ('duration', models.CharField(max_length=5)),
                ('price', models.IntegerField()),
                ('try_see_duration', models.SmallIntegerField()),
                ('video_url', models.CharField(max_length=500, null=True)),
                ('video_url_invalid_at', models.DateTimeField(null=True)),
                ('status', models.SmallIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('curriculum', models.ForeignKey(to='curriculum.Curriculum')),
            ],
            options={
                'db_table': 'video',
            },
        ),
    ]
