# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0003_auto_20151110_2301'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='story',
            options={'verbose_name_plural': 'stories'},
        ),
        migrations.AlterModelOptions(
            name='storypart',
            options={'verbose_name_plural': 'story parts'},
        ),
        migrations.AlterField(
            model_name='story',
            name='session_key',
            field=models.CharField(blank=True, max_length=200, verbose_name='Session key'),
        ),
        migrations.AlterField(
            model_name='storypart',
            name='session_key',
            field=models.CharField(blank=True, max_length=200, verbose_name='Session key'),
        ),
    ]
