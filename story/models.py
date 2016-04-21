from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from mptt.models import MPTTModel, TreeForeignKey

@python_2_unicode_compatible
class Story(models.Model):
    creator = models.ForeignKey(User, verbose_name=_('creator'), related_name="my_stories", blank=True, null=True)
    authors = models.ManyToManyField(User, verbose_name=_('authors'), related_name="stories", blank=True)
    title = models.CharField(max_length=200, verbose_name=_('title'))
    anotation = models.TextField(verbose_name=_('anotation'), blank=True)
    is_finished = models.BooleanField(verbose_name=_('is finished'), default=False)
    is_deleted = models.BooleanField(verbose_name=_('is deleted'), default=False)
    primary_story_line = models.ForeignKey('StoryPart', verbose_name=_('primary story line'), related_name="+", blank=True, null=True)
    created = models.DateTimeField(verbose_name=_('created'), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('updated'), auto_now_add=True)

    class Meta:
        verbose_name_plural = _('stories')

    def __str__(self):
        return "#%s %s" % (self.id, self.title)

    def get_first_part(self):
        return StoryPart.objects.get(story=self, parent__isnull=True)

    def get_absolute_url(self):
        return reverse('story_detail', args=[str(self.pk)])

@python_2_unicode_compatible
class StoryPart(models.Model):
    story = models.ForeignKey(Story, verbose_name=_('story'), related_name="+")
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    text_block = models.ForeignKey(TextBlock, verbose_name=_('text'), related_name="+")
    is_primary = models.BooleanField(verbose_name=_('is primary'), default=False)
    is_deleted = models.BooleanField(verbose_name=_('is deleted'), default=False)
    primary_story_line = models.ForeignKey('self', verbose_name=_('primary story line'), related_name="+", blank=True, null=True)
    created = models.DateTimeField(verbose_name=_('created'), auto_now_add=True)

    class MPTTMeta:
        order_insertion_by = ['created']

    class Meta:
        verbose_name_plural = _('story parts')

    def __str__(self):
        return "%s in %s" % (self.id, self.story)

    def get_absolute_url(self):
        if (self.primary_story_line):
            return reverse('story_detail_by_part', args=[str(self.story.pk), str(self.primary_story_line.pk)])
        else:
            return reverse('story_detail_by_part', args=[str(self.story.pk), str(self.pk)])

    def update_primary_story_line(self, part):
        self.primary_story_line = part
        self.save()
        for p in StoryPart.objects.filter(primary_story_line = self):
            p.primary_story_line = part
            p.save()

@python_2_unicode_compatible
class TextBlock(models.Model):
    story_part = models.ForeignKey(StoryPart, verbose_name=_('story part'), related_name="text_block")
    author = models.ForeignKey(User, verbose_name=_('author'), related_name="parts", blank=True, null=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    diff = models.TextField(verbose_name=_('diff'))
    text = models.TextField(verbose_name=_('text'))
    created = models.DateTimeField(verbose_name=_('created'), auto_now_add=True)

    class Meta:
        verbose_name_plural = _('text blocks')

    def __str__(self):
        return "%s in %s" % (self.id, self.story)

@python_2_unicode_compatible
class StoryLine(models.Model):
    is_primary = models.BooleanField(verbose_name=_('is primary'), default=False)
    created = models.DateTimeField(verbose_name=_('created'), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('updated'), auto_now_add=True)
    parts = models.ManyToManyField(StoryPart, verbose_name=_('parts'), related_name="stories", blank=True)

    class Meta:
        verbose_name_plural = _('stories')

    def __str__(self):
        return "#%s %s" % (self.id, self.title)

    def get_first_part(self):
        return StoryPart.objects.get(story=self, parent__isnull=True)

    def get_absolute_url(self):
        return reverse('story_detail', args=[str(self.pk)])