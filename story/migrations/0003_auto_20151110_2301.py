# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0002_auto_20151110_2258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='anotation',
            field=models.TextField(verbose_name='Anotation', blank=True),
        ),
        migrations.AlterField(
            model_name='storypart',
            name='story',
            field=models.ForeignKey(to='story.Story', verbose_name='Story', related_name='+'),
        ),
    ]
