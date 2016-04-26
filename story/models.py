from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Story(models.Model):
    creator = models.ForeignKey(User, verbose_name=_('creator'), related_name="my_stories", blank=True, null=True)
    authors = models.ManyToManyField(User, verbose_name=_('authors'), related_name="stories", blank=True)
    title = models.CharField(max_length=200, verbose_name=_('title'))
    anotation = models.TextField(verbose_name=_('anotation'), blank=True)
    is_finished = models.BooleanField(verbose_name=_('is finished'), default=False)
    is_deleted = models.BooleanField(verbose_name=_('is deleted'), default=False)
    created = models.DateTimeField(verbose_name=_('created'), auto_now_add=True)

    class Meta:
        verbose_name_plural = _('stories')

    def __str__(self):
        return "#%s %s" % (self.pk, self.title)

    def get_absolute_url(self):
        return ""

@python_2_unicode_compatible
class StoryPart(models.Model):
    story = models.ForeignKey(Story, verbose_name=_('story'), related_name="+")
    level = models.IntegerField(verbose_name=_('level'))
    is_deleted = models.BooleanField(verbose_name=_('is deleted'), default=False)
    created = models.DateTimeField(verbose_name=_('created'), auto_now_add=True)

    class Meta:
        verbose_name_plural = _('story parts')
        ordering = ['story', 'level']

    def __str__(self):
        return "%s in %s" % (self.pk, self.story)

    def get_absolute_url(self):
        return ""

@python_2_unicode_compatible
class TextBlock(models.Model):
    story_part = models.ForeignKey(StoryPart, verbose_name=_('story part'), related_name="text_block")
    author = models.ForeignKey(User, verbose_name=_('author'), related_name="parts", blank=True, null=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    diff = models.TextField(verbose_name=_('diff'), blank=True)
    text = models.TextField(verbose_name=_('text'))
    created = models.DateTimeField(verbose_name=_('created'), auto_now_add=True)

    class Meta:
        verbose_name_plural = _('text blocks')

    def __str__(self):
        return "%s text for %s" % (self.pk, self.story_part)

    def get_absolute_url(self):
        return ""

@python_2_unicode_compatible
class StoryLine(models.Model):
    story = models.ForeignKey(Story, verbose_name=_('story'), related_name="+")
    is_primary = models.BooleanField(verbose_name=_('is primary'), default=False)
    created = models.DateTimeField(verbose_name=_('created'), auto_now_add=True)

    class Meta:
        verbose_name_plural = _('story lines')

    def __str__(self):
        return "%s line #%s" % (self.story, self.pk)

    def get_parts(self):
        return self.parts.objects.sort(story=self, parent__isnull=True)

    def get_absolute_url(self):
        return reverse('story_detail_line', args=[str(self.pk)])
        
@python_2_unicode_compatible
class StoryLinePart(models.Model):
    story_line = models.ForeignKey(StoryLine, verbose_name=_('story line'), related_name="parts")
    story_part = models.ForeignKey(StoryPart, verbose_name=_('story part'), related_name="line_parts")
    text_block = models.ForeignKey(TextBlock, verbose_name=_('text block'), related_name="line_parts")
    created = models.DateTimeField(verbose_name=_('created'), auto_now_add=True)

    class Meta:
        verbose_name_plural = _('story line parts')
        ordering = ['story_line', 'story_part__level']

    def __str__(self):
        return "#%s %s" % (self.pk, self.story_line)

    def get_absolute_url(self):
        #return reverse('story_detail', args=[str(self.pk)])
        return ""