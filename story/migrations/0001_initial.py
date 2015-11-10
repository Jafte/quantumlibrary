# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import taggit.managers
from django.conf import settings
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0002_auto_20150616_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unknown_author_counter', models.IntegerField(default=0, verbose_name='Unknown author counter')),
                ('session_key', models.CharField(verbose_name='Session key', max_length=200)),
                ('title', models.CharField(verbose_name='Title', max_length=200)),
                ('anotation', models.TextField(verbose_name='Anotation')),
                ('is_finished', models.BooleanField(default=False, verbose_name='Is finished')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Is deleted')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now_add=True, verbose_name='Updated')),
                ('authors', models.ManyToManyField(related_name='stories', to=settings.AUTH_USER_MODEL, null=True, verbose_name='Authors', blank=True)),
                ('creator', models.ForeignKey(related_name='my_stories', null=True, blank=True, to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
            ],
        ),
        migrations.CreateModel(
            name='StoryPart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_key', models.CharField(verbose_name='Session key', max_length=200)),
                ('text', models.TextField(verbose_name='Text')),
                ('is_primary', models.BooleanField(default=False, verbose_name='Is primary')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Is deleted')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('author', models.ForeignKey(related_name='parts', null=True, blank=True, to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', null=True, blank=True, to='story.StoryPart')),
                ('primary_story_line', models.ForeignKey(related_name='+', null=True, blank=True, to='story.StoryPart', verbose_name='Primary story line')),
                ('story', models.ForeignKey(related_name='+', verbose_name='Story part', to='story.Story')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='story',
            name='primary_story_line',
            field=models.ForeignKey(related_name='+', null=True, blank=True, to='story.StoryPart', verbose_name='Primary story line'),
        ),
        migrations.AddField(
            model_name='story',
            name='tags',
            field=taggit.managers.TaggableManager(through='taggit.TaggedItem', verbose_name='Tags', help_text='A comma-separated list of tags.', to='taggit.Tag'),
        ),
    ]
