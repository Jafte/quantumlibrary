from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from taggit.managers import TaggableManager
from mptt.models import MPTTModel, TreeForeignKey

@python_2_unicode_compatible
class Story(models.Model):
    creator = models.ForeignKey(User, verbose_name=_('Creator'), related_name="my_stories", blank=True, null=True)
    authors = models.ManyToManyField(User, verbose_name=_('Authors'), related_name="stories", blank=True)
    unknown_author_counter = models.IntegerField(verbose_name=_('Unknown author counter'), default=0)
    session_key = models.CharField(max_length=200, verbose_name=_('Session key'), blank=True)
    created = models.DateTimeField(verbose_name=_('Created'), auto_now_add=True)
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    anotation = models.TextField(verbose_name=_('Anotation'), blank=True)
    is_finished = models.BooleanField(verbose_name=_('Is finished'), default=False)
    is_deleted = models.BooleanField(verbose_name=_('Is deleted'), default=False)
    primary_story_line = models.ForeignKey('StoryPart', verbose_name=_('Primary story line'), related_name="+", blank=True, null=True)
    created = models.DateTimeField(verbose_name=_('Created'), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('Updated'), auto_now_add=True)
    tags = TaggableManager(blank=True)

    class Meta:
        verbose_name_plural = _('stories')

    def __str__(self):
        return "#%s %s" % (self.id, self.title)

    def get_absolute_url(self):
        return reverse('story_detail', args=[str(self.pk)])

@python_2_unicode_compatible
class StoryPart(MPTTModel):
    story = models.ForeignKey(Story, verbose_name=_('Story'), related_name="+")
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    author = models.ForeignKey(User, verbose_name=_('Author'), related_name="parts", blank=True, null=True)
    session_key = models.CharField(max_length=200, verbose_name=_('Session key'), blank=True)
    text = models.TextField(verbose_name=_('Text'))
    is_primary = models.BooleanField(verbose_name=_('Is primary'), default=False)
    is_deleted = models.BooleanField(verbose_name=_('Is deleted'), default=False)
    primary_story_line = models.ForeignKey('self', verbose_name=_('Primary story line'), related_name="+", blank=True, null=True)
    created = models.DateTimeField(verbose_name=_('Created'), auto_now_add=True)

    class MPTTMeta:
        order_insertion_by = ['created']

    class Meta:
        verbose_name_plural = _('story parts')

    def __str__(self):
        return "%s in %s" % (self.id, self.story)