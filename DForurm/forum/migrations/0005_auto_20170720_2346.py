# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-21 04:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0004_remove_post_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='description',
            field=models.TextField(blank=True, default='', max_length=10000),
            preserve_default=False,
        ),
    ]
