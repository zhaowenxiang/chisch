# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0002_video_video_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='video_url_invalid_at',
            field=models.DateTimeField(null=True),
        ),
    ]
